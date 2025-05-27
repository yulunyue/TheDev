from common.algo.export import State, Action
import gym


class Flvo(State):
    _env = None

    def __init__(self, player_id=0, depth=1, state=None):
        super().__init__(player_id, depth, state)
        self.actions = self.__class__.get_env().P[state]
        # self.set_done(done).set_reward(reward)

    @classmethod
    def all_state_key(cls):
        return cls.get_env().P.keys()

    @classmethod
    def get_env(cls):
        if cls._env is None:
            cls._env = gym.make(
                "FrozenLake-v1", render_mode="rgb_array"
            )  # .unwrapped 创建环境
            cls._env.reset()
            cls._env.render()
        return cls._env
