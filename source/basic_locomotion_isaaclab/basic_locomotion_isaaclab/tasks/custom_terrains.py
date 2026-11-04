import numpy as np
import trimesh

from isaaclab.terrains import SubTerrainBaseCfg
from isaaclab.terrains.height_field import HfTerrainBaseCfg
from isaaclab.terrains.height_field.utils import height_field_to_mesh
from isaaclab.utils.configclass import configclass


def overhang_boxes_terrain(difficulty: float, cfg: "MeshOverhangBoxesTerrainCfg") -> tuple[list[trimesh.Trimesh], np.ndarray]:
    """Generate a flat terrain with scattered boxes whose top plate sticks out over the sides (like a mushroom).

    A swing foot hitting the side of a box ends up under the overhang, so it cannot slide up along the riser and
    has to be moved back and lifted higher. The box height and the overhang grow with the difficulty.
    """
    box_height = cfg.box_height_range[0] + difficulty * (cfg.box_height_range[1] - cfg.box_height_range[0])
    overhang = cfg.overhang_range[0] + difficulty * (cfg.overhang_range[1] - cfg.overhang_range[0])
    top_thickness = min(cfg.top_thickness, 0.5 * box_height)

    terrain_height = 1.0
    center = np.array([0.5 * cfg.size[0], 0.5 * cfg.size[1]])
    meshes_list = list()

    # Ground
    ground_pos = (center[0], center[1], -terrain_height / 2)
    meshes_list.append(trimesh.creation.box((cfg.size[0], cfg.size[1], terrain_height),
                                            trimesh.transformations.translation_matrix(ground_pos)))

    # Scatter the boxes outside the central platform, without overlaps (checked on the bounding circles)
    placed = []  # (x, y, radius)
    for _ in range(cfg.num_boxes * 20):
        if len(placed) >= cfg.num_boxes:
            break
        width = np.random.uniform(*cfg.box_width_range)
        half_top = 0.5 * width + overhang
        radius = np.sqrt(2.0) * half_top
        margin = cfg.border_width + radius
        x = np.random.uniform(margin, cfg.size[0] - margin)
        y = np.random.uniform(margin, cfg.size[1] - margin)
        if max(abs(x - center[0]), abs(y - center[1])) < 0.5 * cfg.platform_width + radius:
            continue
        if any(np.hypot(x - px, y - py) < radius + pr + cfg.min_gap for px, py, pr in placed):
            continue
        placed.append((x, y, radius))

        yaw = np.random.uniform(0.0, np.pi / 2)
        rotation = trimesh.transformations.rotation_matrix(yaw, (0.0, 0.0, 1.0))
        # Stem, from the ground to the bottom of the top plate
        stem_height = box_height - top_thickness
        stem = trimesh.creation.box((width, width, stem_height),
                                    trimesh.transformations.translation_matrix((x, y, 0.5 * stem_height)) @ rotation)
        # Top plate, larger than the stem by the overhang on each side
        top = trimesh.creation.box((width + 2.0 * overhang, width + 2.0 * overhang, top_thickness),
                                   trimesh.transformations.translation_matrix(
                                       (x, y, box_height - 0.5 * top_thickness)) @ rotation)
        meshes_list += [stem, top]

    origin = np.array([center[0], center[1], 0.0])
    return meshes_list, origin


@configclass
class MeshOverhangBoxesTerrainCfg(SubTerrainBaseCfg):
    """Configuration for a flat terrain with scattered boxes with an overhanging top plate."""

    function = overhang_boxes_terrain

    num_boxes: int = 20
    """The number of boxes to place (fewer if they do not fit)."""

    box_width_range: tuple[float, float] = (0.3, 0.6)
    """The minimum and maximum width of the box stem (in m)."""

    box_height_range: tuple[float, float] = (0.05, 0.15)
    """The box height at difficulty 0 and 1 (in m)."""

    overhang_range: tuple[float, float] = (0.02, 0.08)
    """How much the top plate sticks out over each side of the stem, at difficulty 0 and 1 (in m)."""

    top_thickness: float = 0.03
    """The thickness of the top plate (in m)."""

    platform_width: float = 2.0
    """The width of the free square platform at the center of the terrain (in m)."""

    border_width: float = 0.25
    """The free border around the terrain (in m)."""

    min_gap: float = 0.3
    """The minimum free distance between two boxes (in m)."""


@height_field_to_mesh
def holes_terrain(difficulty: float, cfg: "HfHolesTerrainCfg") -> np.ndarray:
    """Generate a flat terrain with many small square holes, deep enough that a foot in a hole is catastrophic.

    The holes have a fixed size, independent of the difficulty: the terrain is meant to have many edges to avoid,
    not to be hard to cross.
    """
    width_pixels = int(round(cfg.size[0] / cfg.horizontal_scale))
    length_pixels = int(round(cfg.size[1] / cfg.horizontal_scale))
    # In the mesh a hole of N pixels is (N + 1) pixels wide, since the walls are moved to the neighboring vertices
    hole_pixels = max(1, int(round(cfg.hole_size / cfg.horizontal_scale)) - 1)
    gap_pixels = int(round(cfg.min_gap / cfg.horizontal_scale)) + 1
    platform_pixels = int(round(cfg.platform_width / cfg.horizontal_scale))
    hole_depth = int(round(cfg.hole_depth / cfg.vertical_scale))

    hf_raw = np.zeros((width_pixels, length_pixels), dtype=np.int16)
    # Cells where a hole cannot start: the central platform (grown by the hole size and the gap) and the holes placed
    # so far (grown by the gap), so that the holes are at least min_gap apart and never touch the platform
    blocked = np.zeros((width_pixels, length_pixels), dtype=bool)
    center_x, center_y = width_pixels // 2, length_pixels // 2
    half_platform = platform_pixels // 2
    blocked[
        max(0, center_x - half_platform - hole_pixels - gap_pixels + 1):center_x + half_platform + gap_pixels,
        max(0, center_y - half_platform - hole_pixels - gap_pixels + 1):center_y + half_platform + gap_pixels,
    ] = True

    num_placed = 0
    for _ in range(cfg.num_holes * 20):
        if num_placed >= cfg.num_holes:
            break
        x = np.random.randint(0, width_pixels - hole_pixels + 1)
        y = np.random.randint(0, length_pixels - hole_pixels + 1)
        if blocked[x, y]:
            continue
        hf_raw[x:x + hole_pixels, y:y + hole_pixels] = -hole_depth
        blocked[
            max(0, x - hole_pixels - gap_pixels + 1):x + hole_pixels + gap_pixels,
            max(0, y - hole_pixels - gap_pixels + 1):y + hole_pixels + gap_pixels,
        ] = True
        num_placed += 1

    return hf_raw


@configclass
class HfHolesTerrainCfg(HfTerrainBaseCfg):
    """Configuration for a flat terrain with many small square holes of fixed size."""

    function = holes_terrain

    num_holes: int = 150
    """The number of holes to place (fewer if they do not fit)."""

    hole_size: float = 0.3
    """The side of the square holes (in m), rounded to a multiple of the horizontal scale. With a single pixel (2
    horizontal scales) the walls cannot be vertical and the hole becomes a diagonal slit, so use at least 3."""

    hole_depth: float = 1.0
    """The depth of the holes (in m)."""

    min_gap: float = 0.3
    """The minimum flat distance between two holes, and between a hole and the platform (in m)."""

    platform_width: float = 2.0
    """The width of the flat square platform at the center of the terrain (in m)."""
