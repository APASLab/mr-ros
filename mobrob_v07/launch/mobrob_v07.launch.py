import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def validate_and_use_mode(context, *args, **kwargs):
    pkg_mobrob_localization = get_package_share_directory("mobrob_v07")
    mode_value = LaunchConfiguration("mode").perform(context)
    valid_values = ["localization", "mapping", "navigation"]

    if mode_value not in valid_values:
        print(f"Invalid parameter value: '{mode_value}'. Must be one of {valid_values}.", file=sys.stderr)
        sys.exit(1)

    return [Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", os.path.join(pkg_mobrob_localization, "rviz", f"{mode_value}.rviz")],
        output="screen",
    )]


def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory("gazebo_ros")
    pkg_turtlebot3_gazebo = get_package_share_directory("turtlebot3_gazebo")

    use_sim_time = LaunchConfiguration("use_sim_time", default="true")
    x_pose = LaunchConfiguration("x_pose", default="0.0")
    y_pose = LaunchConfiguration("y_pose", default="0.0")
    mode = DeclareLaunchArgument(
        "mode",
        default_value="localization",
        description="Operating mode. Must be one of ['localization', 'mapping', 'navigation']"
    )

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, "launch", "gzserver.launch.py")
        ),
        launch_arguments={
            "world": os.path.join(pkg_turtlebot3_gazebo, "worlds", "turtlebot3_dqn_stage4.world"),
        }.items()
    )

    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_turtlebot3_gazebo, "launch", "spawn_turtlebot3.launch.py")
        ),
        launch_arguments={
            "x_pose": x_pose,
            "y_pose": y_pose
        }.items()
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_turtlebot3_gazebo, "launch", "robot_state_publisher.launch.py")
        ),
        launch_arguments={"use_sim_time": use_sim_time}.items()
    )

    rviz_cmd = OpaqueFunction(function=validate_and_use_mode)

    return LaunchDescription([
        mode,
        gzserver_cmd,
        spawn_turtlebot_cmd,
        robot_state_publisher_cmd,
        rviz_cmd,
    ])
