from common.algo.export import Action, State
from common.util.export import logger
from .constant import C


class CartAction(Action):
    pass


class CartPoleState(State):
    _env = None

    def __init__(self, state=None, player_id=0, depth=0):
        if CartPoleState._env is None:
            import gymnasium as gym
            from gymnasium.envs.classic_control.cartpole import CartPoleEnv

            CartPoleState._env = gym.make("CartPole-v1", render_mode=C.render_mode)
            CartPoleState._env_ins: CartPoleEnv = CartPoleState._env.env.env.env
        if state is None:
            state, _ = CartPoleState._env.reset()
        self.done = False
        super().__init__(state, player_id, depth)

    def get_sort_actions(self, **kw):

        actions = []
        for i in range(CartPoleState._env.action_space.n):
            CartPoleState._env_ins.state = self.state
            next_state, reward, terminated, _, _ = CartPoleState._env.step(i)
            CartPoleState._env_ins.steps_beyond_terminated = None
            actions.append(
                CartAction(
                    self, i, CartPoleState(next_state).set_done(terminated)
                ).set_reward(reward)
            )
        return actions

    def to_str(self):
        return []

    def render(self):
        CartPoleState._env.state = self.state
        return CartPoleState._env.render()

    def reset(self):
        self.state, _ = CartPoleState._env.reset()
        return super().reset()
