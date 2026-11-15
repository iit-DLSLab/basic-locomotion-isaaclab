from dataclasses import MISSING

from isaaclab.utils.configclass import configclass


@configclass
class StateDecompositionCfg:
    """Mixture of experts: the experts split the state space, and a gate (or the explicit expert index, the last
    observation entry) picks the experts of each sample. All the experts learn the same target.
    """

    who = "actor+critic"
    """Which network uses the mixture of expert: "actor", "critic" or "actor+critic"."""

    num_experts = None
    """The number of expert to use, from 1 to N"""

    gate_hidden_dims = None
    """The dimension of the gate, e.g. [128, 64] or None"""

    top_k = None
    """If not used, put None, otherwise we can do the softmax between 1 to K expert"""

    use_gate_loss = False
    """Regularization loss of the gate to not overspecialize expert"""

    use_load_balance_loss = False
    """Regularization loss of the gate to balance the load between experts"""

    use_explicit_expert = False
    """Whether to use an explicit expert"""

    use_shared_layers = False
    """Whether to use a shared backbone between experts. False, "backbone", "backbone+head" are supported."""

    use_pcgrad = False
    """Project conflicting expert gradients on shared backbones (requires explicit routing)."""

    expert_output_dims = None
    """The output dimensions of each expert, which will be concatenated to form the final output"""


@configclass
class RewardGroupCfg:
    """A group of reward terms, learned by its own critic."""

    terms: list[str] = MISSING
    """fnmatch patterns of the reward term names (the keys of extras["reward_terms"] published by the env), e.g.
    ["feet_*"]. Each term goes to the first group that matches it, so a group with "*" takes all the remaining terms
    and must be the last one."""

    weight: float = 1.0
    """Weight of the group's advantage in the actor loss."""


@configclass
class RewardDecompositionCfg:
    """Multi-critic: the reward is split into groups of terms, each learned by its own critic. All the critics are
    active on every sample, and the actor is trained on the weighted sum of their advantages.
    """

    groups: dict[str, RewardGroupCfg] = MISSING
    """The reward groups, one critic each, e.g. {"feet": RewardGroupCfg(terms=["feet_*"]), "rest": RewardGroupCfg(terms=["*"])}."""

    normalize_advantages: bool = False
    """Normalize each group's advantage before the weighted sum. With False and unit weights the actor sees the
    standard advantage of the total reward (only the critic changes), with True the weights set each group's share of
    the policy gradient."""


@configclass
class MoECfg:
    """Configuration of moe-rsl-rl: state decomposition (mixture of experts) and/or reward decomposition (multi-critic)."""

    class_name: str = "MixtureOfExpert"
    """The class name."""

    decomposition: str = "state"
    """"state" (mixture of experts), "reward" (one critic per reward group) or "state+reward" (both: with
    who="critic" or "actor+critic", every critic of the reward decomposition is a mixture of experts)."""

    state_decomposition_cfg: StateDecompositionCfg | None = None
    """Used if decomposition includes "state", ignored otherwise."""

    reward_decomposition_cfg: RewardDecompositionCfg | None = None
    """Used if decomposition includes "reward", ignored otherwise."""


# Mixture of Expert Stuff
moe_cfg = MoECfg(
    decomposition = "reward",  # "state", "reward" or "state+reward"
    # Used with decomposition = "state" or "state+reward": learned gate (no explicit expert index in the observations)
    state_decomposition_cfg = StateDecompositionCfg(
        who = "actor+critic",
        num_experts = 4,
        gate_hidden_dims = [128],
        top_k = None,
        use_gate_loss = False,
        use_load_balance_loss = False,
        use_explicit_expert = False,
        use_shared_layers = False,
        use_pcgrad = False,
        expert_output_dims = None,
    ),
    # One critic for the feet rewards, one for everything else
    reward_decomposition_cfg = RewardDecompositionCfg(
        groups = {
            "feet": RewardGroupCfg(terms=["feet_*", "*_contact_suggestion"]),
            "rest": RewardGroupCfg(terms=["*"]),
        },
        normalize_advantages = False,
    ),
)
