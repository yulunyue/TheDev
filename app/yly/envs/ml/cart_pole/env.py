from common.algo.export import Action, State
from common.util.export import logger, List
from .constant import C
from common.third_util.torch_util import torch
from common.third_util.np_util import np


class CartAction(Action):
    def do(self):
        if self.dst is not None:  # 用dst会更好，因为reward可能会不存在
            raise Exception("do 2")
        new_state, self.reward, termina, _, _ = CartPoleState.env.step(self.action)
        self.dst = CartPoleState(new_state).set_done(termina)

    def get_dqn_network_params(self, acs: List["CartAction"]):
        states = torch.tensor(np.array([a.src.state for a in acs]), dtype=torch.float)
        actions = torch.tensor([a.action for a in acs]).view(-1, 1)
        rewards = torch.tensor([a.reward for a in acs], dtype=torch.float).view(-1, 1)
        next_states = torch.tensor(
            np.array([(a.dst.state) for a in acs]), dtype=torch.float
        )
        dones = torch.tensor([a.dst.done for a in acs], dtype=torch.float).view(-1, 1)

        # 下个状态的最大Q值

        return states, actions, rewards, dones, next_states


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
