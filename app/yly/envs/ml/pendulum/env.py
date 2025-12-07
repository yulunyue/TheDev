from common.algo.export import Action, State
from common.util.export import logger, List, Dict
from common.third_util.torch_util import torch
from common.third_util.np_util import np
from .constant import C

ENV = None


class QNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = torch.nn.Linear(
            PenduState.env().observation_space.shape[0], C.NET_BASE_HIDDEN_DIM
        )
        self.fc2 = torch.nn.Linear(C.NET_BASE_HIDDEN_DIM, C.ACTION_DIM)

    def forward(self, x):
        x = torch.functional.F.relu(self.fc1(x))
        return self.fc2(x)


class PsAction(Action):
    def do(self):
        e = PenduState.env()
        action_lowbound = e.action_space.low[0]  # 连续动作的最小值
        action_upbound = e.action_space.high[0]  # 连续动作的最大值
        a = action_lowbound + (self.action / (C.ACTION_DIM - 1)) * (
            action_upbound - action_lowbound
        )
        next_state, self.reward, self.done, _, _ = e.step([a])
        e.render()
        self.dst = PenduState(next_state)


class PenduState(State):
    _env = None

    @classmethod
    def env(cls):
        if PenduState._env is None:
            import gymnasium as gym

            PenduState._env = gym.make("Pendulum-v1", render_mode="rgb_array")

        return PenduState._env

    def __init__(self, state=None):
        if state is None:
            state, _ = self.env().reset()
        super().__init__(state)

    def make_actions(self, **kw):
        actions = []
        for i in range(C.ACTION_DIM):
            actions.append(PsAction(self, i))
        return actions

    def reset(self):
        self.state, _ = PenduState.env().reset()
        PenduState._env.render()
        return super().reset()
