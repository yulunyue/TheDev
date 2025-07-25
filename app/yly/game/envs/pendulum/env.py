from common.algo.export import Action, State
from common.util.export import logger


class PenduState(State):
    _env = None

    def __init__(self, state=None, player_id=0, depth=0):
        if PenduState._env is None:
            import gymnasium as gym
            from gymnasium.envs.classic_control.pendulum import PendulumEnv

            PenduState._env = gym.make("Pendulum-v1", render_mode="human")
            PenduState._env_ins: PendulumEnv = PenduState._env.env.env.env
        if state is None:
            state, _ = PenduState._env.reset()
        self.done = False
        super().__init__(state, player_id, depth)

    def state_size(self):
        return PenduState._env.observation_space.shape[0]

    def get_actions(self, depth=1, **kw):
        if self.actions:
            return self.actions
        self.actions = dict()
        for i in range(PenduState._env.action_space.n):
            PenduState._env_ins.state = self.state
            next_state, reward, terminated, _, _ = PenduState._env.step(i)
            self.actions[i] = PenduState(
                self, i, PenduState(next_state).set_done(terminated)
            ).set_reward(reward)
        return self.actions

    def to_str(self):
        return f"{self.state}"

    def render(self):
        PenduState._env.state = self.state
        return PenduState._env.render()

    def reset(self):
        self.state, _ = PenduState._env.reset()
        return super().reset()
