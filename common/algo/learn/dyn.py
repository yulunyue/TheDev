from common.algo.search.algo import Algo, Action, State
from common.util.export import logger
import numpy as np
from typing import List


class PolicyIteration(Algo):
    def load(self, num_episodes=500, theta=0.001, gamma=0.9):
        self.theta = theta
        self.gamma = gamma
        return super().load(num_episodes)

    def get_action_value(self, action: Action, p=1):
        self.state_count += 1
        if action.dst.done is not None:
            r1 = 0  # 后面没有新的状态了，奖励为0
        else:
            r1 = self.gamma * action.dst.value
        return p * (action.reward + action.dst.reward + r1)

    def get_qsa_value(self, qsalst):
        return sum(qsalst)

    def policy_evaluation(self, state_cls: State, max_cnt=-1):
        cnt = 0

        states = state_cls.all_states()
        while max_cnt == -1 or cnt < max_cnt:
            new_values = []
            max_diff = 0
            for src in states:
                qsalst = []
                for action in src.get_actions().values():
                    qsalst.append(self.get_action_value(action, action.p))
                qsa = self.get_qsa_value(qsalst)
                max_diff = max(max_diff, abs(qsa - src.value))
                # src.set_value(qsa)
                new_values.append(qsa)
            for i, v in enumerate(new_values):
                states[i].set_value(v)
            # logger.debug(f"STATES cnt:{cnt}{state_cls.to_str()}")

            cnt += 1
            if max_diff < self.theta:
                break
        logger.info(f"policy_evaluation迭代次数: {cnt}")
        return cnt

    def policy_improvement(self, state_cls: State):  # 策略提升
        cha = 0
        states = state_cls.all_states()
        for s in states:
            actions = list(s.get_actions().values())
            qsa_list = [self.get_action_value(a) for a in actions]
            maxq = max(qsa_list)
            cntq = qsa_list.count(maxq)  # 计算有几个动作得到了最大的Q值
            # 让这些动作均分概率
            for i, q in enumerate(qsa_list):
                p = 1 / cntq if q == maxq else 0
                cha += abs(actions[i].p - p)
                actions[i].set_p(p)
                # logger.info(
                #     f"策略提升 {a.src.state}->{a.action}:{cha} {p} {self.get_action_value(a)} {maxq}"
                # )
        logger.info(f"STATES{state_cls.to_str()}")
        logger.info(f"策略提升完成 cha:{cha}")
        return cha == 0

    def run(self, state_cls: State, max_num=10000):
        turn = 0
        while turn < max_num:
            self.policy_evaluation(state_cls)
            fg = self.policy_improvement(state_cls)
            if fg:
                return turn
            turn += 1
        return self


class ValueIteration(PolicyIteration):
    def get_action_value(self, action, p=1):
        return super().get_action_value(action, 1)

    def get_qsa_value(self, qsalst):
        return max(qsalst)

    def run(self, state: State):
        self.policy_evaluation(state)
        self.policy_improvement(state)
        return self
