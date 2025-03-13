from common.algo.search.algo import Env, Algo, Action, State
import numpy as np


class PolicyIteration(Algo):
    def load(self, K=4 * 12, action_size=4, num_episodes=5000, theta=0.001, gamma=0.9):
        self.theta = theta
        self.k = K
        self.gamma = gamma
        self.v = [0] * self.k
        self.pi = [[1 / action_size] * action_size for _ in range(K)]
        return super().load(num_episodes)

    def get_values(self, v):
        return sum(v)

    def policy_evaluation(self, state: Env, max_cnt=100000):
        cnt = 0
        while cnt < max_cnt:
            max_diff = 0
            new_v = [0] * self.k
            for i in range(self.k):
                qsa_list = []
                s = state.new_state(i)
                for action in s.get_actions():
                    qsa = 0
                    for p, next_state, r in action.get_states():
                        qsa += p * (
                            r
                            + self.gamma
                            * self.v[next_state.state]
                            * (1 - next_state.done)
                        )
                    if self.pi[i]:
                        qsa = self.pi[i][action.key] * qsa
                    qsa_list.append(qsa)
                new_v[i] = self.get_values(qsa_list)
                max_diff = max(max_diff, abs(new_v[i] - self.v[i]))
            self.v = new_v
            cnt += 1
            if max_diff < self.theta:
                break
        return cnt

    def policy_improvement(self, state: State):
        old_pi = self.pi.copy()
        for s in range(self.k):
            qsa_list = []
            for a in state.new_state(s).get_actions():
                qsa = 0
                for p, next_state, r in a.get_states():
                    qsa += p * (
                        r
                        + self.gamma * self.v[next_state.state] * (1 - next_state.done)
                    )
                qsa_list.append(qsa)
            maxq = max(qsa_list)
            cntq = qsa_list.count(maxq)
            self.pi[s] = [1 / cntq if q == maxq else 0 for q in qsa_list]
        return old_pi == self.pi

    def run(self, state: Env):
        records = []
        while True:
            records.append(self.policy_evaluation(state))
            if self.policy_improvement(state):
                break
        return records


class ValueIteration(PolicyIteration):
    def get_values(self, v):
        return max(v)

    def get_policy(self):
        for i in range(self.k):
            pass

    def run(self, state):
        self.pi = [None] * self.k
        ct = self.policy_evaluation(state)
        self.policy_improvement(state)
        return ct
