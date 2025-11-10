from common.algo.export import Action, State
from common.util.export import logger
from .constant import C


class PenduState(State):
    _env = None

    @property
    def env(self):
        if PenduState._env is None:
            import gymnasium as gym

            PenduState._env = gym.make("Pendulum-v1", render_mode="rgb_array")
        return PenduState._env

    def __init__(self, state=None):
        if state is None:
            state, _ = self.env.reset()
        self.done = False
        super().__init__(state)

    def make_actions(self, depth=1, **kw):
        if self.actions:
            return self.actions
        self.actions = dict()
        for i in range(C.n):
            PenduState._env_ins.state = self.state
            next_state, reward, terminated, _, _ = PenduState._env.step(
                C.min + i * C.step
            )
            self.actions[i] = PenduState(
                self, i, PenduState(next_state).set_done(terminated)
            ).set_reward(reward)
        return self.actions

    def to_str(self):
        return f"{self.state}"

    # def reset(self):
    #     self.state, _ = PenduState._env.reset()
    #     return super().reset()
