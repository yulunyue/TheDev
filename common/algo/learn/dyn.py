from common.algo.search.algo import Algo, Action, State
from common.util.export import logger, defaultdict
import numpy as np
from typing import List


class PolicyIteration(Algo):
    def load(self, pi=None, train_epoll=100, num_episodes=1000, theta=0.001, gamma=0.9):
        self.theta = theta
        self.gamma = gamma
        self.train_epoll = train_epoll
        self.pi = pi
        self.num_episodes = num_episodes
        return super().load()

    def reset(self):
        self.v = defaultdict(int)
        return super().reset()

    def get_action_value(self, action: Action):
        return action.get_reward() + self.gamma * self.v[action.get_dst().state]

    def get_qsa_value(self, qsalst):
        return sum(qsalst)

    def policy_evaluation(self, states: List[State]):
        self.p_cnt = 0
        while self.num_episodes > 0 and self.p_cnt < self.num_episodes:
            new_values = defaultdict(int)
            max_diff = 0
            for src in states:
                qsalst = []
                actions = src.get_sort_actions()
                if not actions:
                    continue
                pi = 1 / len(actions)
                for action in actions:
                    if self.pi:
                        pi = self.pi[src.state][action.action]
                    qsalst.append(self.get_action_value(action) * pi)
                new_values[src.state] = self.get_qsa_value(qsalst)
                max_diff = max(max_diff, abs(new_values[src.state] - self.v[src.state]))
            self.v = new_values
            self.p_cnt += 1
            self.log_value(max_diff)
            if max_diff < self.theta:
                break

    def policy_improvement(self, states: List[State]):  # 策略提升
        pi = dict()
        for s in states:
            actions = s.get_sort_actions()
            if not actions:
                continue
            maxq = float("-inf")
            cntq = 0
            for a in actions:
                q = self.get_action_value(a)
                if q > maxq:
                    s.set_best_action(a)
                    maxq = q
                    cntq = 1
                elif q == maxq:
                    cntq += 1
            pi[s.state] = {
                a.action: 1 / cntq if self.get_action_value(a) == maxq else 0
                for a in actions
            }

        return pi

    def train_all_states(self, states: List[State]):
        self.cnt = 0
        while self.cnt < self.train_epoll:
            self.policy_evaluation(states)
            pi = self.policy_improvement(states)
            if self.pi and self.pi == pi:
                break
            self.cnt += 1
            self.pi = pi
            self.log_policy()
        return self

    def log_value(self, diff):
        pass

    def log_policy(self):
        pass


class ValueIteration(PolicyIteration):
    def get_qsa_value(self, qsalst):
        return max(qsalst)

    def train_all_state(self, state: State):
        states = state.bfs().values()
        self.policy_evaluation(states)
        self.policy_improvement(states)
        return self
