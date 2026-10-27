"""Calibration of a stereo depth camera (RealSense D4xx) for its simulated model, tasks/locomotion/realsense_<camera>.py:
the same scene and the same measurements for every camera (D435, D457, ...).

Setup
-----
1. Scene: a flat matte wall or floor, a plain one is fine (the projector of the camera gives it texture), filling the
   whole image, also on the left edge, where the band that the right imager does not see is measured. Nothing else in
   the image. Optionally a box on it near the center of the image, e.g. an 8 cm cube, for the shadow left of it that
   the right imager does not see. No sunlight, emitter on (default of the driver).
2. Camera: fixed (tripod, clamp), facing the wall or the floor roughly perpendicularly. Nothing moves in the image
   during the recording (300 frames: 5 s at 60 fps, 10 s at 30 fps).
3. Distance: the box farther than the minimum depth of the camera (fx * baseline / 126 px of disparity) with margin,
   and the wall far enough for the frame to frame noise to be above the 1 mm unit of the depth:

     camera  stream                decimation to 106x60        baseline   min depth   wall     face of the 8 cm cube
     D435    848x480x60            8                           0.0499 m   0.17 m      0.5 m    0.42 m
     D457    640x360x30 (USB 2.1)  6, 4 columns cropped left   0.0952 m   0.25 m      0.7 m    0.62 m

   Too close, the box has no depth (black in "valid fraction" of the figure) and the script warns that the noise is
   close to the quantization of the depth: move the camera back.
4. Baseline, from the calibration of the camera, with no driver running (it holds the camera):
       rs-enumerate-devices -o | grep "Stereo Baseline"    # [mm]
5. Driver, in the deploy env (pixi shell --manifest-path deploy/installation/pixi.toml -e humble, then
   source deploy/ros2_localhost_connect.sh, in each terminal):
   - D435: bash deploy/camera_connect.sh
   - D457: the same launch at 640x360:
       ros2 launch realsense2_camera rs_launch.py enable_color:=false enable_infra1:=false enable_infra2:=false \
           enable_gyro:=false enable_accel:=false pointcloud.enable:=false enable_sync:=false \
           depth_module.depth_profile:=640x360x30
6. Calibration, recording the depth to run it again later (e.g. after a change of the script) with --load:
       python deploy/calibrate_depth_camera.py --baseline 0.0499 --save d435.npz --figure d435.png
       python deploy/calibrate_depth_camera.py --baseline 0.0952 --save d457.npz --figure d457.png
       python deploy/calibrate_depth_camera.py --baseline 0.0952 --load d457.npz --figure d457.png
   --width/--height for a policy image other than 106x60.

Checks
------
- No WARNING, and the box, if any, with depth in the figure ("mean depth", planes outlined in white).
- Left band: measured - model within about 1 column, otherwise the baseline or the intrinsics are wrong.
- Shadows: the model hides by the pixel centers of the closer surface, so its shadows are about 1 column narrower than
  the measured ones (+1 for the D457 at 0.5-0.7 m). With no box there are no shadows to check.
- The values of the cfg are measured, without margin. realsense_d435.py keeps one: noise_relative_std = 0.01 (the
  accuracy of the datasheet) against 0.005 measured, noise_max_dropout = 0.01 against 0.003.

Method
------
The raw depth is cropped on the left to a multiple of the policy image (inside the band that the right imager does not
see) and decimated by the median of the valid pixels of each block, as decimate_depth of run_sensor2heightmap_ros2.py.
On the decimated depth it measures:
- intrinsics, the values of the cfg;
- minimum depth: the closest valid depth of the raw stream;
- band on the left and shadows left of closer objects, against the model of seen_by_right_imager;
- frame to frame noise on the planes of the scene, as noise_relative_std * z^2, and its part fixed in time;
- random holes per frame on the planes (noise_max_dropout) and isolated valid pixels (false matches).
"""

import argparse
import sys
import time

import matplotlib
import numpy as np
from scipy import ndimage

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def record(topic: str, info_topic: str, num_frames: int) -> tuple[np.ndarray, np.ndarray]:
    """num_frames raw depth images [T, H, W] (16UC1) of topic and the intrinsic matrix [3, 3] of info_topic."""
    import rclpy
    from rclpy.node import Node
    from rclpy.qos import qos_profile_sensor_data
    from sensor_msgs.msg import CameraInfo, Image

    frames, intrinsics = [], []

    def on_depth(msg):
        if msg.encoding == "16UC1" and len(frames) < num_frames:
            frames.append(np.frombuffer(msg.data, dtype=np.uint16).reshape(msg.height, msg.step // 2)[:, :msg.width].copy())

    def on_info(msg):
        if not intrinsics:
            intrinsics.append(np.array(msg.k, dtype=np.float64).reshape(3, 3))

    rclpy.init()
    node = Node("calibrate_depth_camera")
    node.create_subscription(Image, topic, on_depth, qos_profile_sensor_data)
    node.create_subscription(CameraInfo, info_topic, on_info, qos_profile_sensor_data)
    deadline = time.monotonic() + 30.0 + num_frames / 5.0
    while (len(frames) < num_frames or not intrinsics) and time.monotonic() < deadline:
        rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()
    if len(frames) < num_frames or not intrinsics:
        sys.exit(f"Received {len(frames)} 16UC1 depth images on {topic} and {len(intrinsics)} camera_info: is the driver running?")
    return np.stack(frames), intrinsics[0]


def decimate_depth(depth: np.ndarray, factor: int, depth_scale: float) -> np.ndarray:
    """Depth [H, W] (raw units, 0 where invalid) to [H / factor, W / factor] in meters: the median of the valid pixels
    of each factor x factor block, 0 where less than half of them are valid (decimate_depth of
    run_sensor2heightmap_ros2.py)."""
    height, width = depth.shape[0] // factor, depth.shape[1] // factor
    blocks = depth[: height * factor, : width * factor].reshape(height, factor, width, factor).swapaxes(1, 2)
    blocks = np.sort(blocks.reshape(height, width, factor * factor), axis=-1)
    # The invalid pixels (0) sort first: the valid ones are the last n of each block.
    size = factor * factor
    n = np.count_nonzero(blocks, axis=-1)
    low = np.take_along_axis(blocks, np.minimum(size - n + (n - 1) // 2, size - 1)[..., None], -1)[..., 0]
    high = np.take_along_axis(blocks, np.minimum(size - n + n // 2, size - 1)[..., None], -1)[..., 0]
    median = 0.5 * (low.astype(np.float32) + high.astype(np.float32)) * depth_scale
    return np.where(n >= 0.5 * size, median, 0.0).astype(np.float32)


def fit_planes(points: np.ndarray, candidates: np.ndarray, max_planes: int = 10, min_pixels: int = 30) -> np.ndarray:
    """Planes of the scene by RANSAC on points [h, w, 3] (camera frame, m) where candidates [h, w]: labels [h, w] of
    the connected parts of at least min_pixels of each plane, -1 elsewhere."""
    rng = np.random.default_rng(0)
    labels = np.full(candidates.shape, -1)
    remaining = candidates.copy()
    for _ in range(3 * max_planes):
        P = points[remaining]
        if labels.max() + 1 >= max_planes or len(P) < min_pixels:
            break
        tolerance = 0.005 + 0.01 * P[:, 2] ** 2
        best = None
        for _ in range(500):
            sample = P[rng.choice(len(P), 3, replace=False)]
            normal = np.cross(sample[1] - sample[0], sample[2] - sample[0])
            if np.linalg.norm(normal) < 1e-9:
                continue
            normal /= np.linalg.norm(normal)
            inliers = np.abs((P - sample[0]) @ normal) < tolerance
            if best is None or inliers.sum() > best.sum():
                best = inliers
        # Least squares plane of the inliers.
        center = P[best].mean(0)
        normal = np.linalg.svd(P[best] - center)[2][-1]
        on_plane = np.zeros_like(remaining)
        on_plane[remaining] = np.abs((P - center) @ normal) < tolerance
        parts, num_parts = ndimage.label(on_plane)
        sizes = ndimage.sum(on_plane, parts, range(1, num_parts + 1))
        large = 1 + np.flatnonzero(sizes >= min_pixels)
        if large.size == 0:
            # Inliers scattered over other surfaces: drop them and look for the next plane.
            remaining &= ~on_plane
            continue
        # Only the large parts leave the candidates: the other inliers can be on other surfaces, e.g. a box parallel
        # to the floor.
        for part in large:
            labels[parts == part] = labels.max() + 1
        remaining &= ~np.isin(parts, large)
    return labels


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--baseline", type=float, required=True, help="Stereo baseline [m] of the calibration of the camera.")
    parser.add_argument("--width", type=int, default=106, help="Width of the depth image of the policy [px].")
    parser.add_argument("--height", type=int, default=60, help="Height of the depth image of the policy [px].")
    parser.add_argument("--frames", type=int, default=300, help="Number of depth images to record.")
    parser.add_argument("--topic", default="/camera/camera/depth/image_rect_raw")
    parser.add_argument("--info-topic", default="/camera/camera/depth/camera_info")
    parser.add_argument("--depth-scale", type=float, default=0.001, help="Meters per raw depth unit.")
    parser.add_argument("--save", help="Save the recorded depth (.npz).")
    parser.add_argument("--load", help="Calibrate on a recorded depth (.npz) instead of the driver.")
    parser.add_argument("--figure", default="depth_calibration.png")
    args = parser.parse_args()

    if args.load:
        data = np.load(args.load)
        raw, K = data["depth"], data["K"].reshape(3, 3)
    else:
        raw, K = record(args.topic, args.info_topic, args.frames)
        if args.save:
            np.savez_compressed(args.save, depth=raw, K=K)
    stream_height, stream_width = raw.shape[1:]

    # Decimation and crop on the left to the policy image.
    factor = stream_height // args.height
    crop = stream_width - factor * args.width
    if factor < 1 or stream_height != factor * args.height or not 0 <= crop < factor:
        sys.exit(f"A {stream_width}x{stream_height} stream does not decimate to {args.width}x{args.height}")
    depth = np.stack([decimate_depth(frame[:, crop:], factor, args.depth_scale) for frame in raw])
    h, w = args.height, args.width
    fx, fy = K[0, 0] / factor, K[1, 1] / factor
    cx, cy = (K[0, 2] - crop) / factor, K[1, 2] / factor
    focal_baseline = fx * args.baseline

    # Per pixel statistics over the frames, on the valid ones.
    valid = depth > 0
    count = valid.sum(0)
    valid_fraction = count / len(depth)
    mean = depth.sum(0) / np.maximum(count, 1)
    std = np.sqrt((((depth - mean) * valid) ** 2).sum(0) / np.maximum(count, 1))
    ray_x, ray_y = np.meshgrid((np.arange(w) + 0.5 - cx) / fx, (np.arange(h) + 0.5 - cy) / fy)
    ray = np.stack([ray_x, ray_y, np.ones((h, w))], -1)

    # Planes of the scene; their pixels away from the edges are the surfaces of the noise and holes.
    labels = fit_planes(mean[..., None] * ray, valid_fraction >= 0.95)
    surface = np.zeros((h, w), bool)
    plane_depth = np.zeros((h, w))
    for label in np.unique(labels[labels >= 0]):
        part = labels == label
        center = (mean[..., None] * ray)[part].mean(0)
        normal = np.linalg.svd((mean[..., None] * ray)[part] - center)[2][-1]
        plane_depth[part] = (center @ normal) / (ray[part] @ normal)
        surface |= ndimage.binary_erosion(part)
    if surface.sum() < 30:
        sys.exit("No flat surface found: is the scene static, with a wall farther than the minimum depth?")
    z = mean[surface]
    temporal = std[surface] / z**2
    fixed = (mean - plane_depth)[surface]
    quantization = args.depth_scale / np.sqrt(12.0)

    holes = ~valid[:, surface]
    hole_fraction = holes.mean(1)
    persistence = (holes[1:] & holes[:-1]).sum() / max(holes[:-1].sum(), 1)
    neighbours = ndimage.convolve(valid.astype(int), np.array([[[0, 1, 0], [1, 0, 1], [0, 1, 0]]]), mode="constant")
    isolated = (valid & (neighbours == 0)).sum((1, 2))

    # Band on the left and shadows left of closer objects: pixels valid in at least half of the frames against the
    # model, where column u of depth z is seen by the right imager if u + 0.5 - fx * baseline / z >= 0 and no closer
    # point to its right lands left of it.
    seen = valid_fraction >= 0.5
    band_rows, band_measured, band_model, shadow_measured, shadow_model = [], [], [], [], []
    for v in range(h):
        # Runs of at least 3 such pixels starting or ending on a plane, without the false matches and the pixels
        # missing because closer than the minimum depth.
        runs, num_runs = ndimage.label(seen[v])
        solid = [np.flatnonzero(runs == run)[[0, -1]] for run in range(1, num_runs + 1) if (runs == run).sum() >= 3]
        if not solid:
            continue
        first = solid[0][0]
        if (labels[v, first : first + 3] >= 0).any():
            band_rows.append(v)
            band_measured.append(first)
            band_model.append(max(0, int(np.ceil(focal_baseline / np.median(mean[v, first : first + 3]) - 0.5))))
        for (_, end), (start, _) in zip(solid[:-1], solid[1:]):
            far, near = mean[v, end], mean[v, start]
            if (labels[v, end - 2 : end + 1] >= 0).any() and (labels[v, start : start + 3] >= 0).any() and far - near > 0.02:
                # The model hides the far columns u with u + 0.5 - fx * baseline / far >= start + 0.5 - fx * baseline / near.
                shadow_measured.append(start - end - 1)
                shadow_model.append(np.floor(focal_baseline * (1.0 / near - 1.0 / far)))
    band_error = np.array(band_measured) - np.array(band_model)

    # The closest valid depth is the minimum depth of the camera only with something closer in the scene, else the
    # limit of the 126 px of disparity of the D400.
    min_depth = raw[raw > 0].min() * args.depth_scale
    disparity_limit = K[0, 0] * args.baseline / 126
    min_depth_measured = min_depth < 1.1 * disparity_limit
    noise_relative_std = np.median(temporal)
    max_dropout = 2.0 * hole_fraction.mean()
    print(f"\n{stream_width}x{stream_height} stream, {crop} columns cropped on the left, decimated by {factor} to {w}x{h}, {len(depth)} frames")
    print(f"  intrinsics      fx {fx:.3f} fy {fy:.3f} cx {cx:.3f} cy {cy:.3f} ({cx - w / 2:+.3f} / {cy - h / 2:+.3f} px from the image center)")
    print(f"                  FOV {np.degrees(2 * np.arctan(w / 2 / fx)):.1f} x {np.degrees(2 * np.arctan(h / 2 / fy)):.1f} deg")
    print(f"  min depth       closest valid depth {min_depth:.3f} m (D400 limit of 126 px of disparity: {disparity_limit:.3f} m)"
          + ("" if min_depth_measured else ": nothing closer than the minimum depth in the scene, not measured"))
    print(f"  surfaces        {labels.max() + 1} planes, {surface.sum()} px, z {np.percentile(z, 5):.2f}-{np.percentile(z, 95):.2f} m")
    print(f"  temporal noise  std / z^2: median {noise_relative_std:.4f}, rms {np.sqrt(np.mean(temporal**2)):.4f} [1/m]; "
          f"neighbour correlation {np.corrcoef(*_neighbour_pairs(depth, valid, mean, surface))[0, 1]:.2f}")
    print(f"  fixed noise     rms {1000 * np.sqrt(np.mean(fixed**2)):.2f} mm, / z^2 {np.sqrt(np.mean((fixed / z**2) ** 2)):.4f} [1/m] (includes the flatness of the wall)")
    print(f"  random holes    {100 * hole_fraction.mean():.3f}% of the surface per frame (max {100 * hole_fraction.max():.3f}%), "
          f"{100 * persistence:.0f}% still there in the next frame")
    print(f"  isolated pixels {isolated.mean():.2f} per frame (max {isolated.max()}), valid with no valid neighbour")
    low, high = np.percentile(band_error, [10, 90])
    print(f"  left band       measured - model: median {np.median(band_error):+.1f} columns, 10-90% {low:+.1f} {high:+.1f}, over {len(band_error)} rows")
    if shadow_measured:
        shadow_error = np.array(shadow_measured) - np.array(shadow_model)
        low, high = np.percentile(shadow_error, [10, 90])
        print(f"  shadows         {np.median(shadow_measured):.1f} columns, measured - model: median {np.median(shadow_error):+.1f}, "
              f"10-90% {low:+.1f} {high:+.1f}, over {len(shadow_measured)} rows")
    else:
        print("  shadows         none: no object in front of the wall")
    if np.median(std[surface]) < 2.0 * quantization:
        print(f"\n  WARNING: the temporal noise ({1000 * np.median(std[surface]):.2f} mm) is close to the quantization of the "
              f"depth ({1000 * quantization:.2f} mm): move the camera farther from the wall.")
    print(f"""
Values of the cfg (measured, without margin):
    width: int = {w}
    height: int = {h}
    focal_length: float = {0.5 * (fx + fy):.2f}
    min_depth: float = {min_depth if min_depth_measured else disparity_limit:.3f}{"" if min_depth_measured else "  # D400 limit, not measured"}
    baseline: float = {args.baseline:.4f}
    noise_relative_std: float = {noise_relative_std:.4f}
    noise_max_dropout: float = {max_dropout:.4f}  # twice the mean random holes per frame
""")

    fig, ax = plt.subplots(2, 3, figsize=(18, 8.5))
    depth_range = {"vmin": np.percentile(z, 1) * 0.8, "vmax": np.percentile(z, 99) * 1.1}
    image = ax[0, 0].imshow(np.where(count > 0, mean, np.nan), cmap="turbo", **depth_range)
    ax[0, 0].contour(labels, levels=np.arange(labels.max() + 1) + 0.5, colors="w", linewidths=0.8)
    ax[0, 0].set_title("mean depth [m], planes")
    fig.colorbar(image, ax=ax[0, 0])
    image = ax[0, 1].imshow(valid_fraction, cmap="gray", vmin=0, vmax=1)
    ax[0, 1].plot(np.array(band_model) - 0.5, band_rows, "r-", label="band of the model")
    ax[0, 1].legend(loc="lower right")
    ax[0, 1].set_title("valid fraction over the frames")
    fig.colorbar(image, ax=ax[0, 1])
    image = ax[0, 2].imshow(depth[0], cmap="turbo", **depth_range)
    ax[0, 2].set_title("one frame [m], 0 where invalid")
    fig.colorbar(image, ax=ax[0, 2])
    image = ax[1, 0].imshow(np.where(surface, std / np.maximum(mean, 1e-6) ** 2, np.nan), cmap="viridis")
    ax[1, 0].set_title("temporal std / z^2 [1/m]")
    fig.colorbar(image, ax=ax[1, 0])
    limit = np.percentile(np.abs(fixed), 99) * 1000
    image = ax[1, 1].imshow(np.where(surface, mean - plane_depth, np.nan) * 1000, cmap="RdBu", vmin=-limit, vmax=limit)
    ax[1, 1].set_title("fixed in time: mean - plane [mm]")
    fig.colorbar(image, ax=ax[1, 1])
    zz = np.linspace(min(z.min(), 0.2), max(z.max(), 1.0), 50)
    ax[1, 2].plot(z, std[surface] * 1000, ".", ms=2, alpha=0.5, label="pixels of the surfaces")
    ax[1, 2].plot(zz, noise_relative_std * zz**2 * 1000, "r-", label=f"{noise_relative_std:.4f} z^2")
    ax[1, 2].axhline(quantization * 1000, color="k", ls="--", label="quantization of the depth")
    ax[1, 2].set_xlabel("z [m]")
    ax[1, 2].set_ylabel("temporal std [mm]")
    ax[1, 2].legend()
    fig.tight_layout()
    fig.savefig(args.figure, dpi=80)
    print(f"Figure: {args.figure}")


def _neighbour_pairs(depth, valid, mean, surface):
    """Temporal errors of the pairs of horizontal neighbours on the surface, valid in the same frame."""
    pair = surface[:, :-1] & surface[:, 1:]
    both = valid[:, :, :-1] & valid[:, :, 1:] & pair
    error = depth - mean
    return error[:, :, :-1][both], error[:, :, 1:][both]


if __name__ == "__main__":
    main()
