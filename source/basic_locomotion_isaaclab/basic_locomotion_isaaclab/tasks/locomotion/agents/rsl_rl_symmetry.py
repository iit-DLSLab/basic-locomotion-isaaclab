"""Left-right (sagittal) symmetry of the quadruped, for the RSL-RL data augmentation.

:func:`compute_symmetric_states` is the ``data_augmentation_func`` of :class:`RslRlSymmetryCfg`. It appends to the
mini-batch the reflection of every sample about the sagittal (xz) plane of the base:

- vectors (linear velocity, projected gravity) flip y, pseudo-vectors (angular velocity) flip x and z;
- the velocity commands flip the lateral velocity and the yaw rate, the base pose commands flip the roll (height and
  pitch are unchanged);
- the legs swap left and right (FL <-> FR, RL <-> RR) and the joints change sign as set by the env cfg
  ``symmetry_joint_signs``: the hips of Go2, Aliengo, A2 and B2 (hip axes along +x on both sides) change sign, the
  ones of HyQReal and Pegasus (mirrored hip axes on the right legs) keep it, the thighs and the calves keep it.
  Checked with the MJCF forward kinematics of ``robot_model/``: the mirrored configuration is the reflection of the
  original one;
- the per-foot terms (clock, contacts, air/contact time, foot error) swap left and right;
- the height maps flip y. The permutation is computed from the ray pattern, so it does not depend on its ordering.

The actions are offsets from the default joint positions and are mirrored as the joint positions.

Each observation term is mapped by a permutation and a sign, ``mirrored = obs[..., perm] * sign``. They are built once
from the env cfg, following the layout of ``LocomotionEnv._get_observations``: a change of that layout must be
reflected in :func:`_build_proprioceptive_step`, :func:`_build_privileged`, :func:`_build_rma` and
:func:`_build_observation_group`.
"""

from __future__ import annotations

import torch
from tensordict import TensorDict

LEFT_RIGHT_LEGS = {"FL": "FR", "FR": "FL", "RL": "RR", "RR": "RL"}
"""Leg swapped by the sagittal reflection."""

FEET_ORDER = ("FL", "FR", "RL", "RR")
"""Order of the per-foot observation terms."""

JOINT_TYPES = ("hip", "thigh", "calf")


def _mirror_joint_name(name: str) -> str:
    leg = name.split("_", 1)[0]
    return LEFT_RIGHT_LEGS[leg] + name[len(leg) :]


class _MirrorBuilder:
    """Concatenates the permutation and the sign of consecutive observation terms."""

    def __init__(self, joint_signs: dict[str, float]):
        self.joint_signs = joint_signs
        self.perm: list[int] = []
        self.sign: list[float] = []

    def __len__(self) -> int:
        return len(self.perm)

    def add(self, perm, sign):
        offset = len(self.perm)
        self.perm += [offset + int(p) for p in perm]
        self.sign += [float(s) for s in sign]

    def extend(self, other: _MirrorBuilder, repeat: int = 1):
        for _ in range(repeat):
            self.add(other.perm, other.sign)

    def vector(self):
        self.add([0, 1, 2], [1.0, -1.0, 1.0])

    def pseudo_vector(self):
        self.add([0, 1, 2], [-1.0, 1.0, -1.0])

    def invariant(self, size: int):
        self.add(range(size), [1.0] * size)

    def joints(self, names: list[str], signed: bool = True):
        """Joint angles, velocities, actions (signed) or joint parameters such as gains and friction (not signed)."""
        perm = [names.index(_mirror_joint_name(name)) for name in names]
        self.add(perm, [self.joint_signs[name.split("_")[1]] if signed else 1.0 for name in names])

    def per_foot(self, num_terms: int = 1):
        perm = [FEET_ORDER.index(LEFT_RIGHT_LEGS[foot]) for foot in FEET_ORDER]
        for _ in range(num_terms):
            self.add(perm, [1.0] * len(FEET_ORDER))

    def height_map(self, scanner_cfg):
        """Flip y of the height map of a ray caster aligned with the base yaw."""
        if abs(scanner_cfg.offset.pos[1]) > 1e-6:
            raise ValueError(f"The height scanner is not centered on the sagittal plane: offset {scanner_cfg.offset.pos}.")
        pattern_cfg = scanner_cfg.pattern_cfg
        ray_starts, _ = pattern_cfg.func(pattern_cfg, "cpu")
        xy = ray_starts[:, :2].double()
        distance, perm = torch.cdist(xy * torch.tensor([1.0, -1.0], dtype=torch.float64), xy).min(dim=1)
        if distance.max() > 1e-6:
            raise ValueError("The height scanner pattern is not symmetric about the sagittal plane.")
        self.add(perm.tolist(), [1.0] * len(perm))


def _joint_signs(cfg) -> dict[str, float]:
    joint_signs = getattr(cfg, "symmetry_joint_signs", None)
    if joint_signs is None or set(joint_signs) != set(JOINT_TYPES):
        raise ValueError(
            "Set symmetry_joint_signs = {'hip': ..., 'thigh': ..., 'calf': ...} in the env cfg: the sign of each"
            f" joint type after the left-right reflection. Got {joint_signs}."
        )
    return dict(joint_signs)


def _build_proprioceptive_step(env) -> _MirrorBuilder:
    """One step of the proprioceptive history."""
    cfg = env.cfg
    joints = list(cfg.desired_joints_order)

    b = _MirrorBuilder(_joint_signs(cfg))
    b.vector()  # base linear velocity (ground truth, concurrent SE prediction or zeroed IMU acceleration)
    b.pseudo_vector()  # base angular velocity
    b.vector()  # projected gravity
    b.add([0, 1, 2], [1.0, -1.0, -1.0])  # velocity commands: vx, vy, yaw rate
    if env._use_base_pose_commands:
        b.add([0, 1, 2], [1.0, -1.0, 1.0])  # base pose commands: height offset, roll, pitch
    b.joints(joints)  # joint positions
    b.joints(joints)  # joint velocities
    b.joints(joints)  # last actions
    if cfg.use_clock_signal:
        b.per_foot(2)  # sin, cos of the phase of each foot

    if len(b) != cfg.single_observation_space:
        raise ValueError(
            f"The symmetry layout of one observation step has {len(b)} terms, the env has"
            f" {cfg.single_observation_space}: update agents/rsl_rl_symmetry.py."
        )
    return b


def _gains(env) -> _MirrorBuilder:
    """P and D gains, each one in the joint order of its actuator."""
    b = _MirrorBuilder(_joint_signs(env.cfg))
    for _ in ("stiffness", "damping"):
        for joint_type in JOINT_TYPES:
            b.joints(list(env._robot.actuators[joint_type].joint_names), signed=False)
    return b


def _build_privileged(env) -> _MirrorBuilder:
    """custom_observations._get_privileged_observation_asymmetric."""
    b = _gains(env)
    b.vector()  # clean base linear velocity
    b.invariant(2)  # height error, terrain pitch
    b.per_foot(4)  # contacts, air time, contact time, foot height error
    b.height_map(env.cfg.pose_height_scanner)
    return b


def _build_rma(env) -> _MirrorBuilder:
    """custom_observations._get_privileged_observation_rma."""
    if env.cfg.rma_use_latent_space:
        raise NotImplementedError(
            "The RMA latent is a random projection of the privileged observation and has no mirror:"
            " disable the symmetry augmentation or set rma_use_latent_space = False."
        )
    b = _gains(env)
    joints = list(env._robot.joint_names)  # the friction coefficients are in the articulation joint order
    b.joints(joints, signed=False)  # static friction
    b.joints(joints, signed=False)  # viscous friction
    return b


def _build_observation_group(env, group: str) -> _MirrorBuilder:
    cfg = env.cfg
    step = _build_proprioceptive_step(env)
    b = _MirrorBuilder(step.joint_signs)
    b.extend(step, repeat=cfg.history_length)
    if group == "common":
        return b

    if getattr(cfg, "perceptive_height_scanner", None) is not None:
        b.height_map(cfg.perceptive_height_scanner)
    if group == "critic":
        if cfg.use_asymmetric_ppo:
            b.extend(_build_privileged(env))
    elif group == "policy":
        if cfg.use_rma:
            b.extend(_build_rma(env))
    else:
        raise KeyError(f"No symmetry layout for the observation group '{group}'.")
    return b


def _check_symmetric_default_joint_pos(env, joint_signs: dict[str, float]):
    """The observations and the actions are offsets from the default joint positions, so these must be symmetric."""
    names = list(env.cfg.desired_joints_order)
    default_joint_pos = env._robot.data.default_joint_pos
    default_joint_pos = getattr(default_joint_pos, "torch", default_joint_pos)[0, env._ids_joints_order]
    b = _MirrorBuilder(joint_signs)
    b.joints(names)
    mirrored = default_joint_pos[b.perm] * torch.tensor(b.sign, device=default_joint_pos.device)
    if not torch.allclose(mirrored, default_joint_pos, atol=1e-4):
        raise ValueError(
            "The default joint positions are not symmetric, the joint offsets cannot be mirrored:"
            f" {dict(zip(names, default_joint_pos.tolist()))}"
        )


class _SymmetrySpecs:
    """Permutations and signs of the observation groups and of the actions, built once per env."""

    def __init__(self, env):
        joint_signs = _joint_signs(env.cfg)
        _check_symmetric_default_joint_pos(env, joint_signs)
        self._env = env
        self._observations: dict[str, tuple[torch.Tensor, torch.Tensor]] = {}
        actions = _MirrorBuilder(joint_signs)
        actions.joints(list(env.cfg.desired_joints_order))
        self.actions = self._to_tensors(actions)

    def _to_tensors(self, b: _MirrorBuilder) -> tuple[torch.Tensor, torch.Tensor]:
        device = self._env.device
        return torch.tensor(b.perm, dtype=torch.long, device=device), torch.tensor(b.sign, device=device)

    def observation(self, group: str, size: int) -> tuple[torch.Tensor, torch.Tensor]:
        if group not in self._observations:
            b = _build_observation_group(self._env, group)
            if len(b) != size:
                raise ValueError(
                    f"The symmetry layout of the observation group '{group}' has {len(b)} terms, the env returns"
                    f" {size}: update agents/rsl_rl_symmetry.py."
                )
            self._observations[group] = self._to_tensors(b)
        return self._observations[group]


def _mirror(data: torch.Tensor, perm: torch.Tensor, sign: torch.Tensor) -> torch.Tensor:
    return data[..., perm.to(data.device)] * sign.to(data.device, data.dtype)


@torch.no_grad()
def compute_symmetric_states(env, obs: TensorDict | None = None, actions: torch.Tensor | None = None):
    """Append the left-right mirror of the observations and of the actions to the batch.

    Args:
        env: The RSL-RL environment wrapper.
        obs: The observation groups, shape (batch, ...) each. Defaults to None.
        actions: The joint actions, shape (batch, 12). Defaults to None.

    Returns:
        The observations and the actions with batch size 2 * batch (originals first, then the mirrored ones),
        or None if the respective input is None.
    """
    env = env.unwrapped
    specs = getattr(env, "_symmetry_specs", None)
    if specs is None:
        specs = env._symmetry_specs = _SymmetrySpecs(env)

    obs_aug = None
    if obs is not None:
        obs_aug = TensorDict(
            {
                group: torch.cat((data, _mirror(data, *specs.observation(group, data.shape[-1]))), dim=0)
                for group, data in obs.items()
            },
            batch_size=[2 * obs.batch_size[0]],
            device=obs.device,
        )

    actions_aug = None
    if actions is not None:
        actions_aug = torch.cat((actions, _mirror(actions, *specs.actions)), dim=0)

    return obs_aug, actions_aug
