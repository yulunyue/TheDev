import gymnasium as gym
from common.algo.export import State


class LackState:
    _env: gym.Env = None

    @property
    def env(self):
        if not LackState._env:
            LackState._env = gym.make("FrozenLake-v0")
        return LackState._env
