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
        super().__init__(state)

    def make_actions(self, **kw):
        actions = []
        for i in range(C.n):
            next_state, reward, terminated, _, _ = self.env.step(C.min + i * C.step)
            ns = PenduState(next_state).set_done(terminated)
            actions.append(Action(self, i, ns).set_reward(reward))
        return actions

    def to_str(self):
        return f"{self.state}"

    def reset(self):
        self.state, _ = PenduState._env.reset()
        return super().reset()
