import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_mobrob_3d_perception = get_package_share_directory("mobrob_v04")

    pkg_gazebo_ros = get_package_share_directory("gazebo_ros")
    pkg_turtlebot3_gazebo = get_package_share_directory("turtlebot3_gazebo")
    pkg_turtlebot3_description = get_package_share_directory("turtlebot3_description")

    x_pose = LaunchConfiguration("x_pose", default="0.0")
    y_pose = LaunchConfiguration("y_pose", default="0.0")

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, "launch", "gzserver.launch.py")
        ),
        launch_arguments={
            "world": os.path.join(pkg_mobrob_3d_perception, "models", "empty_world.world"),
        }.items(),
    )

    spawn_turtlebot_cmd = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-entity", "burger",
            "-file", os.path.join(pkg_turtlebot3_gazebo, "models", "turtlebot3_burger", "model.sdf"),
            "-x", x_pose,
            "-y", y_pose,
            "-z", "0.01",
        ],
        output="screen",
    )

    robot_state_publisher_cmd = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{
            "use_sim_time": True,
            "robot_description":  Command([
                "xacro ",
                os.path.join(pkg_turtlebot3_description, "urdf", "turtlebot3_burger.urdf"),
                " namespace:=''"
            ])
        }],
        # arguments=[os.path.join(pkg_turtlebot3_description, "urdf", "turtlebot3_burger.urdf")],
    )

    rviz_cmd = Node(
        name="rviz2",
        package="rviz2",
        executable="rviz2",
        arguments=["-d", os.path.join(pkg_mobrob_3d_perception, "rviz", "mobrob_v04.rviz")],
    )

    mobrob_v04 = Node(
        package="mobrob_v04",
        executable="mobrob_v04",
        name="mobrob_v04",
        output="screen"
    )

    # TODO: Add solution node
    # node_cmd = Node(...)

    return LaunchDescription([
        gzserver_cmd,
        spawn_turtlebot_cmd,
        robot_state_publisher_cmd,
        rviz_cmd,
        mobrob_v04,
        # node_cmd,  # TODO: uncomment
    ])
