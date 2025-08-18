from common.algo.export import State, Action
from .model.constant import C


class Flvo(State):
    _env = None

    def __init__(self, state=None):
        if state is None:
            state = Flvo.get_env().reset()[0]
        super().__init__(state)

    @classmethod
    def get_env(cls):
        if Flvo._env is None:
            from gymnasium.envs.toy_text.frozen_lake import (
                FrozenLakeEnv,
                generate_random_map,
            )
            import gymnasium as gym

            cls.desc = generate_random_map(
                size=C.map_size, p=C.proba_frozen, seed=C.seed
            )
            env = gym.make(
                "FrozenLake-v1",
                render_mode="rgb_array",
                is_slippery=C.is_slippery,
                desc=cls.desc,
            )  # .unwrapped 创建环境
            Flvo._env: FrozenLakeEnv = env.env.env.env
        return Flvo._env

    def make_actions(self, depth=1, **kw):
        actions = dict()
        for a in range(Flvo._env.action_space.n):
            Flvo._env.s = self.state
            next_state, reward, _, _, _ = Flvo._env.step(a)
            actions[a] = Action(self, a, Flvo.new(next_state)).set_reward(reward)
        return actions

    def to_str(self):
        self.get_env()
        # ret = str(self.get_env().desc)
        return "\n".join(
            [" ".join(v).replace("H", "#").replace("F", ".") for v in self.desc]
        )
