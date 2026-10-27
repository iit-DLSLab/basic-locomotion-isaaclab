"""Intel RealSense D457 depth camera: intrinsics, range and noise of the real camera, measured with
deploy/calibrate_depth_camera.py.

The stereo model is the one of the D435: realsense_d435_noise and seen_by_right_imager of realsense_d435.py take this cfg.
"""

from __future__ import annotations

from isaaclab.utils.configclass import configclass

from basic_locomotion_isaaclab.tasks.locomotion.realsense_d435 import RealSenseD435Cfg


@configclass
class RealSenseD457Cfg(RealSenseD435Cfg):
    """Depth stream of a RealSense D457 at 640x360, 4 columns cropped on the left and decimated by 6 to 106x60.

    Intrinsics read from the camera (serial 342622302179, over USB it reports itself as a D455): at 640x360
    fx = fy = 326.35, cx = 322.37, cy = 182.31, 88.9 x 57.8 degrees. The 4 columns beyond 6 * 106 are cropped on the left,
    inside the band that the right imager does not see, and the median of each 6x6 block with at least half of its pixels
    valid gives fx = fy = 54.39 at 106x60 (decimate_depth of deploy/calibrate_depth_camera.py, the robot must do the
    same). The principal point is 0.06 px right and 0.39 px below the image center (0.4 degrees), here at the center as
    for the D435.
    """

    stream_width: int = 640
    """Width of the depth stream of the camera [px] (depth_module.depth_profile:=640x360x30, the most at 640x360 on
    USB 2.1)."""

    stream_height: int = 360
    """Height of the depth stream of the camera [px]."""

    decimation: int = 6
    """Decimation of the stream after cropping its 4 columns beyond decimation * width on the left."""

    width: int = 106
    """Image width [px], (stream_width - 4) / decimation."""

    height: int = 60
    """Image height [px], stream_height / decimation."""

    focal_length: float = 54.39
    """Focal length fx = fy [px]."""

    min_depth: float = 0.25
    """Closer pixels have no depth [m]: measured 0.248 m at 640x360, the 126 px of disparity of the D400
    (fx * baseline / 126 = 0.247 m)."""

    baseline: float = 0.0952
    """Stereo baseline [m], from the calibration of the camera (95.22 mm). The left band that the right imager does not
    see, 5.2 / z columns of the 106, matches the measured one; the bands left of closer objects are about 1 column
    narrower than the measured ones."""

    noise_relative_std: float = 0.0025
    """White noise std growing with the square of the depth, noise_relative_std * z^2 [1/m]: 2.5 mm at 1 m, 1 cm at
    2 m, twice the measured as for the D435. Measured at 106x60 on a floor at 0.67-0.72 m: 0.0012-0.0013 * z^2 from frame
    to frame, correlated 0.6 between horizontal neighbours, plus about 1.1 mm fixed in time, not modeled."""

    noise_max_dropout: float = 0.01
    """Random holes: each image loses a fraction of its pixels drawn uniformly up to this. Measured: under 0.01% of the
    pixels per frame on the floor and on a wall, kept at the value of the D435 as a margin for worse surfaces than
    these."""
