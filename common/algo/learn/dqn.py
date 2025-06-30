from .sarsa import Qlearning, Action, State, np
import torch
import torch.nn.functional as F
import collections
import random


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
    def load(self, learning_rate=2e-3, **kw):
        self.q_net = Qnet(4, 128, 2)
        self.target_q_net = Qnet(4, 128, 2)
        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=learning_rate)
        self.count = 0
        self.replay_buffer = ReplayBuffer(10000)
        return super().load(**kw)

    def do_action(self, a):
        a.do()
        self.reward_tmp_all += a.reward
        self.replay_buffer.add(a.src.state, a.action, a.reward, a.dst.state, a.dst.done)
        if self.replay_buffer.size() > 400:
            self.update_net(**self.replay_buffer.sample(64))
        if a.dst.done:
            return a
        return self.take_action(a.dst)

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
        if self.count % 10:
            self.target_q_net.load_state_dict(self.q_net.state_dict())
        self.count += 1
