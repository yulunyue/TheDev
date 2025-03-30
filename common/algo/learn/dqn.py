from common.algo.search.algo import Env, Algo, Action, State
import numpy as np
from torch import nn
import torch


class Dqn(Algo):
    def load(
        self,
        env_init_fun=None,
        model_fun=None,
        num_episodes=1000,
        gamma_discount=0.9,
        epsilon=0.1,
        alpha=0.5,
        **kw
    ):
        self.env_init_fun = env_init_fun
        self.model_fun = model_fun
        self.gamma_discount = gamma_discount
        self.alpha = alpha
        self.epsilon = epsilon
        return super().load(num_episodes=num_episodes)

    def run_step(self, episode):
        last_state = self.env.init_state
        action = self.epsilon_greedy_policy(last_state, self.env.get_actions())
        rewards_sum = 0
        ct = 0
        game_over = 0
        while not game_over:
            game_over, reward, next_state = self.env.do(last_state, action)
            rewards_sum += reward
            next_action = self.epsilon_greedy_policy(next_state, self.env.get_actions())
            self.update_qtable(last_state, action, reward, next_state, next_action)
            action, last_state = next_action, next_state
            ct += 1
        return rewards_sum, ct, game_over

    def epsilon_greedy_policy(self, state, actions):
        decide_explore_exploit = np.random.random()
        if decide_explore_exploit < self.epsilon:
            action = np.random.choice(len(actions))
        else:
            action = np.argmax(self.q_table[state])
        return action

    def update_qtable(self, state, action, reward, next_state, next_action):
        next_reward = self.gamma_discount * self.q_table[next_state, next_action]
        self.q_table[state, action] = (
            self.alpha * (reward + next_reward)
            + (1 - self.alpha) * self.q_table[state, action]
        )

    def train(self):
        # 初始化主网络和目标网络
        policy_net: nn.Module = self.model_fun()
        target_net: nn.Module = self.model_fun()

        # 训练循环
        for episode in range(self.num_episodes):
            state: State = self.env_init_fun()
            while state.done < 0:
                # ε-greedy选择动作
                if np.random.rand() < self.epsilon:
                    action = state.get_random_action()
                else:
                    q_values = policy_net(state)
                    action = torch.argmax(q_values).item()
                break
                # 执行动作，获取新状态和奖励
                # next_state, reward, done = action.dst, action.reward

                # 存储经验
            #     replay_buffer.add(state, action, reward, next_state, done)

            #     # 从回放缓冲区采样并训练
            #     batch = replay_buffer.sample(BATCH_SIZE)
            #     # 计算Q目标值并更新网络（略）

            # # 定期同步目标网络
            # if episode % TARGET_UPDATE == 0:
            #     target_net.load_state_dict(policy_net.state_dict())
