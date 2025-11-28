from common.algo.learn.sarse.qlearning import Qlearning, Action, State, np
from common.third_util.torch_util import torch
from common.util.export import File, logger, random


class Dqn(Qlearning):
    """
    https://hrl.boyuai.com/
    """

    def set_model(
        self, model, target_update=10, batch_size=64, minimal_size=500, **kw
    ) -> "Dqn":
        self.target_update = target_update
        self.batch_size = batch_size
        self.minimal_size = minimal_size
        self.q_net: torch.nn.Module = model()
        self.target_q_net: torch.nn.Module = model()
        # self.replay_buffer = ReplayBuffer(10000)
        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=self.lr)
        return self

    def reset(self):
        self.actions = []

    def update_action(self, a0: Action):
        self.actions.append(a0)
        if len(self.actions) >= self.minimal_size:
            self.update_net_work(
                *a0.get_dqn_network_params(random.sample(self.actions, self.batch_size))
            )

    def update_net_work(
        self,
        states: torch.Tensor,
        actions: torch.Tensor,
        rewards: torch.Tensor,
        dones: torch.Tensor,
        next_states: torch.Tensor,
    ):
        q_values: torch.Tensor = self.q_net(states)
        # logger.map(s=states.shape, q=q_values.shape, a=actions.shape)
        q_values = q_values.gather(1, actions)  # Q值
        max_next_q_values = self.calc_max_next_q_values(next_states)
        q_targets = rewards + self.gamma * max_next_q_values * (1 - dones)  # TD误差目标
        dqn_loss = torch.mean(
            torch.nn.functional.mse_loss(q_values, q_targets)
        )  # 均方误差损失函数
        self.optimizer.zero_grad()  # PyTorch中默认梯度会累积,这里需要显式将梯度置为0
        dqn_loss.backward()  # 反向传播更新参数
        self.optimizer.step()

        if self.steps % self.target_update == 0:
            self.target_q_net.load_state_dict(self.q_net.state_dict())

    def calc_max_next_q_values(self, next_states):
        max_next_q_values: torch.Tensor = self.target_q_net(next_states)
        return max_next_q_values.max(1)[0].view(-1, 1)

    def get_max_q_action(self, s: State):
        states = torch.tensor(s.state, dtype=torch.float)
        values: torch.Tensor = self.q_net(states)
        return s.get_action(values.argmax().item())


class DoubleDqn(Dqn):
    def calc_max_next_q_values(self, next_states):
        max_action = self.q_net(next_states).max(1)[1].view(-1, 1)
        return self.target_q_net(next_states).gather(1, max_action)
