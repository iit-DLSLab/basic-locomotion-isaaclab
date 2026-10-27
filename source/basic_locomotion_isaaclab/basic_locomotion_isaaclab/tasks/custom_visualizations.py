from __future__ import annotations

import torch

import isaaclab.sim as sim_utils
from isaaclab.markers import VisualizationMarkers, VisualizationMarkersCfg

from .custom_rewards import _compute_edge_map, _get_riser_grid, _has_edge_map


def _set_debug_vis_impl(self, debug_vis: bool):
    show_edge_map = debug_vis and getattr(self.cfg, "visualize_edge_map", False) and _has_edge_map(self)
    if show_edge_map and self._edge_map_visualizer is None:
        marker_radius = getattr(self.cfg, "edge_map_visualization_dot_radius", 0.015)
        edge_map_marker_cfg = VisualizationMarkersCfg(
            prim_path="/Visuals/EdgeMap",
            markers={
                "feasible": sim_utils.SphereCfg(
                    radius=marker_radius,
                    visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 1.0, 1.0)),
                ),
                "not_feasible": sim_utils.SphereCfg(
                    radius=marker_radius,
                    visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 0.0, 0.0)),
                ),
            },
        )
        self._edge_map_visualizer = VisualizationMarkers(edge_map_marker_cfg)
    if self._edge_map_visualizer is not None:
        self._edge_map_visualizer.set_visibility(show_edge_map)

    show_swing_zone = debug_vis and getattr(self.cfg, "visualize_feet_edge_swing_zone", False) and _has_edge_map(self)
    if show_swing_zone and self._feet_edge_swing_visualizer is None:
        # A swing foot is penalized by feet_edge_swing as soon as its sphere enters one of these cylinders, which
        # surround each riser top cell up to feet_edge_swing_margin in front of the riser face. The cylinder height
        # is set per riser when visualizing, so the prototype is 1 m high.
        zone_radius = 0.5 * self._edge_height_scanner.cfg.pattern_cfg.resolution + getattr(
            self.cfg, "feet_edge_swing_margin", 0.04
        )
        feet_edge_swing_marker_cfg = VisualizationMarkersCfg(
            prim_path="/Visuals/FeetEdgeSwingZone",
            markers={
                "zone": sim_utils.CylinderCfg(
                    radius=zone_radius,
                    height=1.0,
                    visual_material=sim_utils.PreviewSurfaceCfg(
                        diffuse_color=(1.0, 0.0, 0.0),
                        opacity=getattr(self.cfg, "feet_edge_swing_visualization_opacity", 0.3),
                    ),
                ),
            },
        )
        self._feet_edge_swing_visualizer = VisualizationMarkers(feet_edge_swing_marker_cfg)
    if self._feet_edge_swing_visualizer is not None:
        self._feet_edge_swing_visualizer.set_visibility(show_swing_zone)

    show_height_map = (
        debug_vis
        and getattr(self.cfg, "visualize_height_map_with_noise", False)
        and getattr(self.cfg, "perceptive_height_scanner", None) is not None
    )
    if show_height_map and self._height_map_visualizer is None:
        marker_radius = getattr(self.cfg, "height_map_visualization_dot_radius", 0.015)
        height_map_marker_cfg = VisualizationMarkersCfg(
            prim_path="/Visuals/HeightMap",
            markers={
                # the terrain hit by the perceptive height scanner
                "clean": sim_utils.SphereCfg(
                    radius=marker_radius,
                    visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 1.0, 0.0)),
                ),
                # the terrain as seen by the policy, with the observation noise
                "noisy": sim_utils.SphereCfg(
                    radius=marker_radius,
                    visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 0.0, 0.0)),
                ),
            },
        )
        self._height_map_visualizer = VisualizationMarkers(height_map_marker_cfg)
    if self._height_map_visualizer is not None:
        self._height_map_visualizer.set_visibility(show_height_map)


def _debug_vis_callback(self, event):
    if self._height_map_visualizer is not None and self._height_map_visualizer.is_visible():
        _visualize_height_map_with_noise(self)
    if not _has_edge_map(self):
        return
    if self._edge_map_visualizer is not None and self._edge_map_visualizer.is_visible():
        _visualize_edge_map(self)
    if self._feet_edge_swing_visualizer is not None and self._feet_edge_swing_visualizer.is_visible():
        _visualize_feet_edge_swing_zone(self)


def _visualize_height_map_with_noise(self):
    # The policy observation is only available after the first step
    obs_buf = getattr(self, "obs_buf", None)
    if obs_buf is None or "policy" not in obs_buf:
        return

    scanner = self._perceptive_height_scanner
    clean = scanner.data.ray_hits_w.clone()
    num_rays = clean.shape[1]

    # The height map is the last term of the policy observation, before the RMA one
    rma_size = self.cfg.rma_output_space if self.cfg.use_rma else 0
    height_map_end = obs_buf["policy"].shape[1] - rma_size
    height_data = obs_buf["policy"][:, height_map_end - num_rays:height_map_end]

    # Back from the observation (scanner height - hit height - 0.5) to the hit height in the world
    noisy = clean.clone()
    noisy[..., 2] = scanner.data.pos_w[:, 2].unsqueeze(1) - 0.5 - height_data

    translations = torch.cat((clean.reshape(-1, 3), noisy.reshape(-1, 3)), dim=0)
    marker_indices = torch.cat(
        (
            torch.zeros(clean.shape[0] * num_rays, dtype=torch.long, device=self.device),
            torch.ones(noisy.shape[0] * num_rays, dtype=torch.long, device=self.device),
        )
    )
    valid_hits = torch.isfinite(translations).all(dim=1)
    if not torch.any(valid_hits):
        return

    self._height_map_visualizer.visualize(
        translations=translations[valid_hits], marker_indices=marker_indices[valid_hits]
    )


def _visualize_feet_edge_swing_zone(self):
    riser_top, riser_top_height, riser_base_height, _ = _get_riser_grid(self)
    riser_top = riser_top.reshape(-1)
    riser_xy = self._edge_height_scanner.data.ray_hits_w[..., :2].reshape(-1, 2)
    valid_riser = riser_top & torch.isfinite(riser_xy).all(dim=1)

    # From the floor at the base of the riser up to the height below which feet_edge_swing penalizes the foot bottom
    zone_top = riser_top_height.reshape(-1) - getattr(self.cfg, "feet_edge_swing_height_margin", 0.01)
    zone_bottom = riser_base_height.reshape(-1)

    # Every grid cell gets a marker so that their number does not change, the cells that are not risers are hidden
    # with a zero scale
    translations = torch.zeros(riser_top.shape[0], 3, device=self.device)
    translations[valid_riser, :2] = riser_xy[valid_riser]
    translations[:, 2] = 0.5 * (zone_top + zone_bottom)
    scales = torch.zeros_like(translations)
    scales[valid_riser, :2] = 1.0
    scales[valid_riser, 2] = (zone_top - zone_bottom)[valid_riser]

    self._feet_edge_swing_visualizer.visualize(translations=translations, scales=scales)


def _visualize_edge_map(self):
    edge_map, _, _, _ = _compute_edge_map(self)
    translations = self._edge_height_scanner.data.ray_hits_w.reshape(-1, 3).clone()
    marker_indices = edge_map.reshape(-1).long()

    valid_hits = torch.isfinite(translations).all(dim=1)
    if not torch.any(valid_hits):
        return

    translations = translations[valid_hits]
    translations[:, 2] += getattr(self.cfg, "edge_map_visualization_height_offset", 0.02)
    marker_indices = marker_indices[valid_hits]

    self._edge_map_visualizer.visualize(translations=translations, marker_indices=marker_indices)
