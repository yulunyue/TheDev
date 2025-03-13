from common.algo.search.algo import Env, Algo, Action, State
import numpy as np


class Dqn(Algo):
    def load(self, num_episodes=1000, gamma_discount=0.9, epsilon=0.1, alpha=0.5):
        self.gamma_discount = gamma_discount
        self.alpha = alpha
        self.q_table = np.zeros((self.env.size, len(self.env.actions)))
        return super().load(num_episodes, epsilon)

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
