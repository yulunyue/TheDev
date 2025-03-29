from common.algo.search.algo import Algo, State, Action
from torch import nn
import torch
import numpy as np


class PrioritizedReplayBuffer:
    def __init__(self):
        self.buffer = []
        self.priorities = []

    def add(self, experience):
        max_prio = max(self.priorities) if self.buffer else 1.0
        self.buffer.append(experience)
        self.priorities.append(max_prio)

    def sample(self, batch_size, alpha=0.6):
        probs = np.array(self.priorities) ** alpha
        probs /= probs.sum()
        indices = np.random.choice(len(self.buffer), batch_size, p=probs)
        return [self.buffer[i] for i in indices]


class Ln(Algo):
    def load(self, model_fun, env_init, use_cache=False):
        self.model_fun = model_fun
        self.env_init = env_init
        return super().load(use_cache)

    def train(self, num=1000):
        model: nn.Module = self.model_fun()
        target_model: nn.Module = self.model_fun()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        buffer = PrioritizedReplayBuffer()
        for episode in range(num):
            # 数据收集阶段
            action: Action = self.env_init()

            while action.dst.done < 0:
                action_probs = model.get_action_probs(state)
                action = np.random.choice(7, p=action_probs)
                next_state, reward, done = env.step(action)
                buffer.add((state, action, reward, next_state, done))
                state = next_state

            # 每200步更新一次
            if episode % 200 == 0:
                batch = buffer.sample(512)
                states = torch.stack([x[0] for x in batch])
                actions = torch.tensor([x[1] for x in batch])
                rewards = torch.tensor([x[2] for x in batch])

                # 计算目标价值
                with torch.no_grad():
                    _, target_values = target_model(next_states)
                targets = rewards + 0.99 * target_values * (1 - dones)

                # 更新网络
                _, values = model(states)
                loss = F.mse_loss(values, targets)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                # 软更新目标网络
                for param, target_param in zip(
                    model.parameters(), target_model.parameters()
                ):
                    target_param.data.copy_(
                        0.01 * param.data + 0.99 * target_param.data
                    )
