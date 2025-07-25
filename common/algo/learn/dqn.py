from common.algo.learn.sarse.qlearning import Qlearning, Action, State, np
import torch
import torch.nn.functional as F
import collections
import random
from common.util.fp import File


class Qnet(torch.nn.Module):
    def __init__(self, state_dim, hidden_dim, action_dim, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fc1 = torch.nn.Linear(state_dim, hidden_dim)
        self.fc2 = torch.nn.Linear(hidden_dim, action_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)


class ReplayBuffer:
    """经验回放池"""

    def __init__(self, capacity):
        self.buffer = collections.deque(maxlen=capacity)  # 队列,先进先出

    def add(self, state, action, reward, next_state, done):  # 将数据加入buffer
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):  # 从buffer中采样数据,数量为batch_size
        transitions = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = zip(*transitions)
        return dict(
            states=np.array(state),
            actions=action,
            rewards=reward,
            next_states=np.array(next_state),
            dones=done,
        )

    def size(self):  # 目前buffer中数据的数量
        return len(self.buffer)


class Dqn(Qlearning):
    def load(
        self, state_dim, hidden_dim, action_dim, learning_rate=2e-3, **kw
    ) -> "Dqn":
        super().load(**kw)
        self.q_net = Qnet(state_dim, hidden_dim, action_dim)
        self.target_q_net = Qnet(state_dim, hidden_dim, action_dim)
        if self.cache and File(self.cache).exists():
            data = torch.load(self.cache)
            self.target_q_net.load_state_dict(data)
            self.q_net.load_state_dict(data)
        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=learning_rate)
        self.replay_buffer = ReplayBuffer(10000)
        return self

    def update_action(self, a: Action):
        self.replay_buffer.add(a.src.state, a.action, a.reward, a.dst.state, a.dst.done)
        if self.replay_buffer.size() > 500:
            self.update_net(**self.replay_buffer.sample(64))

    def get_max_action(self, state: State):
        s = torch.tensor(np.array([state.state]), dtype=torch.float)
        action = self.q_net(s).argmax().item()
        return state.get_action(action)

    def update_net(self, states, actions, next_states, rewards, dones):
        states = torch.tensor(states, dtype=torch.float)
        actions = torch.tensor(actions).view(-1, 1)
        rewards = torch.tensor(rewards, dtype=torch.float).view(-1, 1)
        next_states = torch.tensor(next_states, dtype=torch.float)
        dones = torch.tensor(dones, dtype=torch.float).view(-1, 1)

        q_values = self.q_net(states).gather(1, actions)
        max_next_q_values = self.target_q_net(next_states).max(1)[0].view(-1, 1)
        q_targets = rewards + self.gamma * max_next_q_values * (1 - dones)
        dqn_loss = torch.mean(F.mse_loss(q_values, q_targets))  # 均方误差损失函数
        self.optimizer.zero_grad()  # PyTorch中默认梯度会累积,这里需要显式将梯度置为0
        dqn_loss.backward()  # 反向传播更新参数
        self.optimizer.step()
        if self.state_count % 10:
            self.target_q_net.load_state_dict(self.q_net.state_dict())

    def run_one(self, state):
        if self.cache:
            File(self.cache).make_dir_if_not_exist()
            torch.save(self.q_net.state_dict(), self.cache)
        return super().run_one(state)
