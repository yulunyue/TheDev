from common.algo.search.algo import Algo, Action, State
from common.algo.math_util import atan, sigmoid
from common.util.export import logger
import numpy as np
from typing import List


class PolicyIteration(Algo):
    def load(self, num_episodes=500, theta=0.001, gamma=0.9):
        self.theta = theta
        self.gamma = gamma
        return super().load(num_episodes)

    def get_action_value(self, action: Action):
        if action.dst.done is not None:
            r1 = 0  # 后面没有新的状态了，奖励为0
        else:
            r1 = self.gamma * action.dst.value
        return action.p * (action.reward + action.dst.reward + r1)

    def policy_evaluation(self, states: List[State], max_cnt=-1):
        cnt = 0
        diff_result = []
        while max_cnt == -1 or cnt < max_cnt:
            new_values = []
            max_diff = 0
            for src in states:
                qsa = 0
                for action in src.get_actions().values():
                    qsa += self.get_action_value(action)
                max_diff = max(max_diff, abs(qsa - src.value))
                # src.set_value(qsa)
                new_values.append([src, qsa])

            for src, v in new_values:
                src.set_value(v)
            diff_result.append(max_diff)
            cnt += 1
            if max_diff < self.theta:
                break

        logger.info(f"policy_evaluation迭代次数: {cnt}")
        return cnt, diff_result

    def policy_improvement(self, states: List[State]):
        result = True
        for src in states:
            mx = float("-inf")
            acs = []
            for a in src.get_actions().values():
                v = self.get_action_value(a)
                if v > mx:
                    mx = v
                    acs = [a]
                elif v == mx:
                    acs.append(a)
                a.p = 0
            for a in acs:
                p = 1 / len(acs)
                if p != a.p:
                    a.set_p(p)
                    result = False
        return result

    def run(self, state: List[State]):
        for i in range(10):
            self.policy_evaluation(state)
            if self.policy_improvement(state):
                return i
        return -1


class ValueIteration(PolicyIteration):
    def get_values(self, v):
        return max(v)

    def get_policy(self):
        for i in range(self.k):
            pass

    def run(self, state: State):
        self.pi = [None] * state.all_state_num
        ct = self.policy_evaluation(state)
        self.policy_improvement(state)
        return ct
