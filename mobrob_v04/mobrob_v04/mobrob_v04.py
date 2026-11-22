import os
import time

import rclpy
from rclpy.node import Node

from ros_gz_interfaces.msg import Entity
from ros_gz_interfaces.srv import DeleteEntity, SetEntityPose, SpawnEntity
from geometry_msgs.msg import PoseStamped

from ament_index_python.packages import get_package_share_directory


WORLD_NAME = "default"
PILLAR_POSITION = (2.0, 0.0, 1.0)


class MobRob3dPerception(Node):
    def __init__(self):
        super().__init__("mobrob_v04")

        self.pkg_share_dir = get_package_share_directory("mobrob_v04")

        self.spawn_model("unit_cylinder", "pillar.sdf")

        # Creating subscriber for 2D goal pose
        self.create_subscription(PoseStamped, "/goal_pose", self.move_pillar_callback, 10)

    def spawn_model(self, model_name, model_filename):
        self.get_logger().warning(f"Trying to spawn model: {model_name}")

        # Removing a leftover model
        try:
            self.delete_model(model_name)
        except Exception as _:
            # Failure just means there was nothing there
            pass

        # Loading pillar model
        model = SpawnEntity.Request()
        model.entity_factory.name = model_name
        sdf_path = os.path.join(self.pkg_share_dir, "models", model_filename)
        model.entity_factory.sdf = open(sdf_path, "r").read()
        model.entity_factory.pose.position.x = PILLAR_POSITION[0]
        model.entity_factory.pose.position.y = PILLAR_POSITION[1]
        model.entity_factory.pose.position.z = PILLAR_POSITION[2]
        model.entity_factory.pose.orientation.w = 1.0

        # Creating a service client
        spawn_model_client = self.create_client(SpawnEntity, f"/world/{WORLD_NAME}/create")

        while not spawn_model_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warning(f"Service /world/{WORLD_NAME}/create not available, waiting again...")

        for _ in range(30):
            future = spawn_model_client.call_async(model)
            while not future.done():
                rclpy.spin_once(self)

            if future.result().success:
                self.get_logger().info("Model spawned")
                return

            self.get_logger().warning("Spawn refused, Gazebo is probably still loading the world...")
            time.sleep(1.0)

        self.get_logger().error(f"Could not spawn model: {model_name}")

    def delete_model(self, model_name):
        entity = DeleteEntity.Request()
        entity.entity.name = model_name
        entity.entity.type = Entity.MODEL

        delete_model_client = self.create_client(DeleteEntity, f"/world/{WORLD_NAME}/remove")
        while not delete_model_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warning(f"Service /world/{WORLD_NAME}/remove not available, waiting again...")

        future = delete_model_client.call_async(entity)
        while not future.done():
            rclpy.spin_once(self)

        return future.result().success

    def move_pillar_callback(self, msg):
        if msg.pose.position is None:
            return

        new_pillar_position = SetEntityPose.Request()
        new_pillar_position.entity.name = "unit_cylinder"
        new_pillar_position.entity.type = Entity.MODEL
        new_pillar_position.pose.position.x = msg.pose.position.x
        new_pillar_position.pose.position.y = msg.pose.position.y
        new_pillar_position.pose.position.z = PILLAR_POSITION[2]
        new_pillar_position.pose.orientation.w = 1.0

        entity_pose = self.create_client(SetEntityPose, f"/world/{WORLD_NAME}/set_pose")
        while not entity_pose.wait_for_service(timeout_sec=1.0):
            self.get_logger().warning(f"Service /world/{WORLD_NAME}/set_pose not available, waiting again...")

        entity_pose.call_async(new_pillar_position)


def main(args=None):
    rclpy.init(args=args)

    mobrob_3d_perception = MobRob3dPerception()
    try:
        rclpy.spin(mobrob_3d_perception)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    except Exception as e:
        mobrob_3d_perception.get_logger().error(str(e))
    finally:
        mobrob_3d_perception.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
