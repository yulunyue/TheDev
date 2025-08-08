from common.algo.export import State, Action
from .model.constant import C


class Flvo(State):
    _env = None
    _fe_ins = None

    def __init__(self, state=None):
        if Flvo._env is None:
            from gymnasium.envs.toy_text.frozen_lake import (
                FrozenLakeEnv,
                generate_random_map,
            )
            import gymnasium as gym

            Flvo._env = gym.make(
                "FrozenLake-v1",
                render_mode="rgb_array",
                is_slippery=C.is_slippery,
                desc=generate_random_map(
                    size=C.map_size, p=C.proba_frozen, seed=C.seed
                ),
            )  # .unwrapped 创建环境
            Flvo._fe_ins: FrozenLakeEnv = Flvo._env.env.env.env

        if state is None:
            state = Flvo._env.reset(seed=C.seed)[0]
        super().__init__(state)

    def get_actions(self, depth=1, **kw):
        if self.actions is not None:
            return self.actions
        self.actions = dict()
        for a in range(Flvo._env.action_space.n):
            Flvo._fe_ins.s = self.state
            next_state, reward, _, _, _ = Flvo._env.step(a)
            self.actions[a] = Action(self, a, Flvo(next_state)).set_reward(reward)
        return self.actions
