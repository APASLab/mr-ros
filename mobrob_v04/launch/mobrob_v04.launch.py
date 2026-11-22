import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_mobrob_v04 = get_package_share_directory("mobrob_v04")

    pkg_ros_gz_sim = get_package_share_directory("ros_gz_sim")
    pkg_turtlebot3_gazebo = get_package_share_directory("turtlebot3_gazebo")
    pkg_turtlebot3_description = get_package_share_directory("turtlebot3_description")

    x_pose = LaunchConfiguration("x_pose", default="0.0")
    y_pose = LaunchConfiguration("y_pose", default="0.0")

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            "gz_args": [
                "-r -s -v2 ",
                os.path.join(pkg_mobrob_v04, "models", "empty_world.world"),
            ],
            "on_exit_shutdown": "true",
        }.items(),
    )

    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_turtlebot3_gazebo, "launch", "spawn_turtlebot3.launch.py")
        ),
        launch_arguments={
            "x_pose": x_pose,
            "y_pose": y_pose,
        }.items(),
    )

    service_bridge_cmd = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="service_bridge",
        arguments=[
            "/world/default/create@ros_gz_interfaces/srv/SpawnEntity",
            "/world/default/remove@ros_gz_interfaces/srv/DeleteEntity",
            "/world/default/set_pose@ros_gz_interfaces/srv/SetEntityPose",
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
        arguments=["-d", os.path.join(pkg_mobrob_v04, "rviz", "mobrob_v04.rviz")],
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
        service_bridge_cmd,
        robot_state_publisher_cmd,
        rviz_cmd,
        mobrob_v04,
        # node_cmd,  # TODO: uncomment
    ])
