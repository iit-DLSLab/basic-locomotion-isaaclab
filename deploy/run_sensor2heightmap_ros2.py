import os

# Fail-safe: se non è stato scelto esplicitamente altro,
# ROS 2 comunica solamente sulla macchina locale.
os.environ.setdefault("ROS_LOCALHOST_ONLY", "1")

# ROS 2 imports
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image

# Python imports
import time
import numpy as np

import config


def decimate_depth(depth: np.ndarray, factor: int, min_valid_fraction: float = 0.5, depth_scale: float = 0.001) -> np.ndarray:
    """Depth [H, W] (raw units, 0 where invalid) to [H / factor, W / factor] in meters: the median of the valid pixels
    of each factor x factor block, 0 where less than min_valid_fraction of them are valid.

    The decimation filter of the RealSense driver averages the valid pixels of a block instead, so a block of the
    invalid band on the left with a single false match keeps its depth, meters off: about 2 such pixels per frame at
    848x480 -> 106x60, against 0.1 with this filter, which loses about 2% of the valid pixels.
    """
    height, width = depth.shape[0] // factor, depth.shape[1] // factor
    blocks = depth[: height * factor, : width * factor].reshape(height, factor, width, factor).swapaxes(1, 2)
    blocks = np.sort(blocks.reshape(height, width, factor * factor), axis=-1)
    # The invalid pixels (0) sort first: the valid ones are the last n of each block.
    size = factor * factor
    n = np.count_nonzero(blocks, axis=-1)
    low = np.take_along_axis(blocks, np.minimum(size - n + (n - 1) // 2, size - 1)[..., None], -1)[..., 0]
    high = np.take_along_axis(blocks, np.minimum(size - n + n // 2, size - 1)[..., None], -1)[..., 0]
    median = 0.5 * (low.astype(np.float32) + high.astype(np.float32)) * depth_scale
    return np.where(n >= min_valid_fraction * size, median, 0.0).astype(np.float32)


class DepthToHeightmapROS2(Node):
    """RealSense depth (deploy/camera_connect.sh, 848x480) decimated to the depth camera of the policy (106x60), for
    the height map of the policy. The height map is not computed yet."""

    def __init__(self):
        super().__init__('DepthToHeightmapROS2')

        # Depth camera of the policy (depth_camera_d435 of go2_env_cfg.py); the policies exported before the D435 model
        # have the same 106x60 camera.
        d435 = config.training_env.get("depth_camera_d435", {"width": 106, "height": 60})
        self.depth_width, self.depth_height = d435["width"], d435["height"]
        # Last decimated depth [height, width] in meters, 0 where invalid.
        self.depth_image = None
        self.first_message_depth_arrived = False
        self._last_depth_warning_time = 0.0

        # Subscribers and Publishers
        self.subscription_depth = self.create_subscription(
            Image, "/camera/camera/depth/image_rect_raw", self.get_depth_callback, qos_profile_sensor_data
        )
        # The decimated depth (32FC1, m), to look at it and record it.
        self.publisher_depth = self.create_publisher(Image, "/depth_decimated", 1)


    def get_depth_callback(self, msg):
        """Decimate the RealSense depth (16UC1, mm) to the depth camera of the policy."""
        factor = msg.width // self.depth_width
        if msg.encoding != "16UC1" or factor < 1 or (msg.width, msg.height) != (factor * self.depth_width, factor * self.depth_height):
            # Throttle the warnings, e.g. a camera launched with the decimation filter of the driver.
            now = time.monotonic()
            if now - self._last_depth_warning_time >= 2.0:
                self.get_logger().warning(
                    f"Ignoring a {msg.width}x{msg.height} {msg.encoding} depth: expected 16UC1 at a multiple of "
                    f"{self.depth_width}x{self.depth_height} (848x480, deploy/camera_connect.sh)"
                )
                self._last_depth_warning_time = now
            return
        depth = np.frombuffer(msg.data, dtype=np.uint16).reshape(msg.height, msg.step // 2)[:, :msg.width]
        self.depth_image = decimate_depth(depth, factor)

        depth_msg = Image()
        depth_msg.header = msg.header
        depth_msg.height, depth_msg.width = self.depth_image.shape
        depth_msg.encoding = "32FC1"
        depth_msg.step = 4 * depth_msg.width
        depth_msg.data = self.depth_image.tobytes()
        self.publisher_depth.publish(depth_msg)

        if not self.first_message_depth_arrived:
            self.get_logger().info(f"Received the first depth image ({msg.width}x{msg.height}, decimated by {factor})")
        self.first_message_depth_arrived = True


#---------------------------
if __name__ == '__main__':

    rclpy.init()
    depth_to_heightmap_ros2_node = DepthToHeightmapROS2()
    rclpy.spin(depth_to_heightmap_ros2_node)

    depth_to_heightmap_ros2_node.destroy_node()
    rclpy.shutdown()
