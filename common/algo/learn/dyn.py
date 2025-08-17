from common.algo.search.algo import Algo, Action, State
from common.algo.learn.base import Base
from common.util.export import logger, defaultdict
import numpy as np
from typing import List


class PolicyIteration(Base):
    def load(self, pi, num_episodes=500, theta=0.001, gamma=0.9):
        self.theta = theta
        self.gamma = gamma
        self.v = defaultdict(int)
        self.pi = pi
        return super().load(num_episodes)

    def get_action_value(self, action: Action):
        return action.get_reward() + self.gamma * self.v[action.dst.state]

    def get_qsa_value(self, qsalst):
        return sum(qsalst)

    def policy_evaluation(self, states: List[State], max_cnt=-1):
        cnt = 0
        while max_cnt == -1 or cnt < max_cnt:
            new_values = defaultdict(int)
            max_diff = 0
            for src in states:
                qsalst = []
                for action in src.get_actions().values():
                    qsalst.append(
                        self.get_action_value(action)
                        * self.pi[src.state][action.action]
                    )
                if not qsalst:
                    continue
                new_values[src.state] = self.get_qsa_value(qsalst)
                max_diff = max(max_diff, abs(new_values[src.state] - self.v[src.state]))
            self.v = new_values

            cnt += 1
            if max_diff < self.theta:
                break
        self.log_value(cnt, max_diff)
        return cnt

    def log_value(self, cnt, max_diff):
        pass

    def log_policy(self):
        pass

    def policy_improvement(self, states: List[State]):  # 策略提升
        pi = dict()
        for s in states:
            if s.get_done():
                continue
            actions = list(s.get_actions().values())
            qsa_list = [self.get_action_value(a) for a in actions]
            maxq = max(qsa_list)
            cntq = qsa_list.count(maxq)  # 计算有几个动作得到了最大的Q值
            pi[s.state] = [1 / cntq if q == maxq else 0 for q in qsa_list]
        self.log_policy()
        return pi

    def train(self, state_cls: State):
        states = state_cls.new().bfs().values()
        while True:
            self.policy_evaluation(states)
            pi = self.policy_improvement(states)
            if self.pi and self.pi == pi:
                break
            self.pi = pi


class ValueIteration(PolicyIteration):
    def get_qsa_value(self, qsalst):
        return max(qsalst)
