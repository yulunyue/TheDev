from common.algo.search.algo import Algo, Action, State
from common.util.export import logger, defaultdict
from common.third_util.np_util import np
from typing import List


class PolicyIteration(Algo):
    def set_pi(self, pi):
        self.pi = pi
        return self

    def load(self, train_epoll=100, num_episodes=1000, theta=0.001, gamma=0.9):
        self.theta = theta
        self.gamma = gamma
        self.train_epoll = train_epoll
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
        while self.num_episodes < 0 or self.p_cnt < self.num_episodes:
            new_values = defaultdict(int)
            max_diff = 0
            for src in states:
                qsalst = []
                actions = src.get_sort_actions()
                if not actions:
                    continue
                for action in actions:
                    pi = self.pi[src.state][action.action]
                    qsalst.append(self.get_action_value(action) * pi)
                new_values[src.state] = self.get_qsa_value(qsalst)
                max_diff = max(max_diff, abs(new_values[src.state] - self.v[src.state]))
            self.v = new_values
            self.p_cnt += 1

            if max_diff < self.theta:
                break
        self.log_value(max_diff)

    def policy_improvement(self, states: List[State]):  # 策略提升
        pi = self.pi.copy()
        for s in states:
            values = [self.get_action_value(a) for a in s.get_sort_actions()]
            if not values:
                continue
            maxq = float("-inf")
            cntq = 0
            for q in values:
                if q > maxq:
                    maxq = q
                    cntq = 1
                elif q == maxq:
                    cntq += 1
            pi[s.state] = []
            for a in values:
                if a == maxq:
                    pi[s.state].append(1 / cntq)
                else:
                    pi[s.state].append(0)
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
