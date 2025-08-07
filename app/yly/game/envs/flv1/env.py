from common.algo.export import State, Action
from .model.constant import C


class Flvo(State):
    _env = None

    @classmethod
    def new(cls, state=None):
        env = cls.get_env()
        if state is None:
            state = cls._env.reset(seed=C.seed)[0]
        s = Flvo(state)
        s.actions = dict()
        for a in range(env.action_space):
            cls._fe_ins.s = s.state
            next_state, reward, _, _, _ = env.step(a)
            s.actions[a] = Action(s, a, Flvo.new(next_state)).set_reward(reward)

    @classmethod
    def get_env(cls):
        if cls._env is None:
            from gymnasium.envs.toy_text.frozen_lake import (
                FrozenLakeEnv,
                generate_random_map,
            )
            import gymnasium as gym

            cls._env = gym.make(
                "FrozenLake-v1",
                render_mode="rgb_array",
                is_slippery=C.is_slippery,
                desc=generate_random_map(
                    size=C.map_size, p=C.proba_frozen, seed=C.seed
                ),
            )  # .unwrapped 创建环境
            cls._fe_ins: FrozenLakeEnv = cls._env.env.env.env
        return cls._env
