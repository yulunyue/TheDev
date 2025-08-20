from common.algo.search.algo import Algo, Action, State
from common.algo.learn.base import Base
from common.util.export import logger, defaultdict
import numpy as np
from typing import List


class PolicyIteration(Base):
    def load(self, pi=None, num_episodes=500, theta=0.001, gamma=0.9):
        self.theta = theta
        self.gamma = gamma
        self.pi = pi
        return super().load(num_episodes)

    def reset(self):
        self.v = defaultdict(int)
        return super().reset()

    def get_action_value(self, action: Action):
        return action.get_reward() + self.gamma * self.v[action.get_dst().state]

    def get_qsa_value(self, qsalst):
        return sum(qsalst)

    def policy_evaluation(self, states: List[State], max_cnt=-1):
        cnt = 0
        while max_cnt == -1 or cnt < max_cnt:
            new_values = defaultdict(int)
            max_diff = 0
            for src in states:
                qsalst = []
                actions = list(src.get_actions().values())
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

            cnt += 1
            if max_diff < self.theta:
                break
        self.log_value(cnt, max_diff)
        return cnt

    def log_value(self, cnt, max_diff):
        self.log(f"cnt:{cnt},value:{dict(self.v)}")

    def log_policy(self, pi):
        self.log(f"pi:{dict(pi)}")

    def policy_improvement(self, states: List[State]):  # 策略提升
        pi = dict()
        for s in states:
            if s.get_done():
                continue
            actions = list(s.get_actions().values())
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
        self.log_policy(pi)
        return pi

    def train(self, state_cls: State):
        states = state_cls.bfs().values()
        while True:
            self.policy_evaluation(states)
            pi = self.policy_improvement(states)
            if self.pi and self.pi == pi:
                break
            self.pi = pi
        return self


class ValueIteration(PolicyIteration):
    def get_qsa_value(self, qsalst):
        return max(qsalst)

    def train(self, state_cls):
        states = state_cls.bfs().values()
        self.policy_evaluation(states)
        self.policy_improvement(states)
        return self
