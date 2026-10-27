"""Intel RealSense D435 depth camera: intrinsics, range and noise of the real camera.

The same camera is in iekf-quadruped-isaaclab (tasks/locomotion/realsense_d435.py), whose visual odometry adds the same
noise with realsense_noise of iekf_jax/learning/vo/vo_network.py.
"""

from __future__ import annotations

import torch
from isaaclab.sensors import patterns
from isaaclab.utils.configclass import configclass


@configclass
class RealSenseD435Cfg:
    """Depth stream of a RealSense D435 at 848x480, decimated by 8 to 106x60.

    Intrinsics read from the camera (serial 233522075454): at 848x480 fx = fy = 425.49, cx = 424.46, cy = 239.01,
    89.8 x 58.9 degrees (not the nominal 87 degrees of the datasheet). The robot decimates it by 8
    (decimate_depth of deploy/run_sensor2heightmap_ros2.py: the median of each 8x8 block with at least half of its
    pixels valid), fx = fy = 53.19
    with the principal point within 0.12 px of the image center, where it is here and in MuJoCo.
    """

    stream_width: int = 848
    """Width of the depth stream of the camera [px] (depth_module.depth_profile of deploy/camera_connect.sh)."""

    stream_height: int = 480
    """Height of the depth stream of the camera [px]."""

    decimation: int = 8
    """Decimation of the stream on the robot (decimate_depth of deploy/run_sensor2heightmap_ros2.py)."""

    width: int = 106
    """Image width [px], stream_width / decimation."""

    height: int = 60
    """Image height [px], stream_height / decimation."""

    focal_length: float = 53.19
    """Focal length fx = fy [px]."""

    min_depth: float = 0.2
    """Closer pixels have no depth [m], about the minimum range of the D435 at 848x480."""

    max_depth: float = 10.0
    """Farther pixels have no depth [m]."""

    baseline: float = 0.0499
    """Stereo baseline [m], from the calibration of the camera. The depth is the one of the left imager: the points that
    the right imager does not see have no depth, those outside its image (the left band, 2.7 / z columns of the 106) and
    those behind a closer surface (a band left of every object closer than its background)."""

    enable_noise: bool = True
    """Whether the depth read for training gets the noise below (scripts/dagger, scripts/depth_to_heightmap)."""

    noise_relative_std: float = 0.01
    """White noise std growing with the square of the depth, noise_relative_std * z^2 [1/m]: 1 cm at 1 m, 4 cm at 2 m,
    the accuracy of the datasheet. Measured at 106x60 between 0.27 and 0.53 m: about 0.005 * z^2 from frame to frame
    (white in time, nearly in space), plus about 2 mm fixed in time, not modeled."""

    noise_max_dropout: float = 0.01
    """Random holes: each image loses a fraction of its pixels drawn uniformly up to this. Measured: 0.1-0.2% of the
    pixels per frame, the other holes being where the right imager does not see."""

    def pattern_cfg(self) -> patterns.PinholeCameraPatternCfg:
        """Pattern of the ray-caster camera, principal point at the image center (pixel centers at u + 0.5)."""
        return patterns.PinholeCameraPatternCfg.from_intrinsic_matrix(
            intrinsic_matrix=[
                self.focal_length, 0.0, self.width / 2, 0.0, self.focal_length, self.height / 2, 0.0, 0.0, 1.0
            ],
            width=self.width,
            height=self.height,
        )


def seen_by_right_imager(depth: torch.Tensor, cfg: RealSenseD435Cfg) -> torch.Tensor:
    """Pixels [..., H, W] of the depth whose point the right imager sees. The point of column u lands at
    x = u + 0.5 - focal_length * baseline / z in the right image: it is outside it for x < 0, and hidden for a point
    to its right that lands at or left of x, which is closer."""
    inf = torch.tensor(float("inf"), device=depth.device, dtype=depth.dtype)
    column = torch.arange(depth.shape[-1], device=depth.device, dtype=depth.dtype) + 0.5
    x = torch.where(depth > 0.0, column - cfg.focal_length * cfg.baseline / depth.clamp_min(1e-6), -inf)
    # Leftmost landing of the points to the right of each pixel.
    landing = torch.where(depth > 0.0, x, inf).flip(-1).cummin(-1).values.flip(-1)
    right_of = torch.cat((landing[..., 1:], inf.expand_as(landing[..., :1])), -1)
    return (x >= 0.0) & (right_of > x)


def realsense_d435_noise(depth: torch.Tensor, cfg: RealSenseD435Cfg) -> torch.Tensor:
    """D435-like depth [..., H, W] from the clean ray-cast one (distance to the image plane [m], 0 where nothing is
    hit): white noise growing with the square of the depth, random holes, no depth where the right imager does not see
    and none outside [min_depth, max_depth]. Invalid pixels are 0, as from the camera."""
    noisy = depth + cfg.noise_relative_std * depth**2 * torch.randn_like(depth)
    # One dropout rate per image.
    rate = cfg.noise_max_dropout * torch.rand((*depth.shape[:-2], 1, 1), device=depth.device, dtype=depth.dtype)
    keep = torch.rand_like(depth) >= rate
    valid = (depth > 0.0) & keep & seen_by_right_imager(depth, cfg) & (noisy >= cfg.min_depth) & (noisy <= cfg.max_depth)
    return torch.where(valid, noisy, torch.zeros_like(noisy))
