from common.algo.export import Action, State
from common.util.export import logger
from .constant import C


class CartAction(Action):
    def get_dst(self):
        new_state, self.reward, termina, _, _ = CartPoleState.env.step(self.action)
        logger.debug([self, termina])
        return CartPoleState(new_state).set_done(termina)


class CartPoleState(State):
    env = None

    def __init__(self, state=None):
        if state is None:
            import gymnasium as gym

            CartPoleState.env = gym.make("CartPole-v1", render_mode=C.render_mode)
            self.reset()

        super().__init__(state)

    def get_sort_actions(self, **kw):
        actions = []
        for i in range(CartPoleState.env.action_space.n):
            actions.append(CartAction(self, i))
        return actions

    def reset(self):
        self.state, _ = CartPoleState.env.reset()
        self.done = False
        return super().reset()
