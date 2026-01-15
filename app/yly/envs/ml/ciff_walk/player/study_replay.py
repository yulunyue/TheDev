from common.algo.export import Algo, State, Action
from common.util.export import defaultdict, random, inf
from common.third_util.np_util import np


class RealTimeValueIteration(Algo):
    def load(self):
        self.epsilon = 0.1
        self.gamma = 0.9
        self.model = dict()
        self.v = defaultdict(float)
        self.set_train_epoll(100)
        return super().load()

    def update(self, state, action, next_state, reward):
        """更新模型并局部价值迭代"""
        # 保存经验
        self.model[state][action].append((reward, next_state))

        # 实时价值迭代（只更新相关状态）
        states_to_update = self.get_relevant_states(state)
        self.local_value_iteration(states_to_update)

    def get_relevant_states(self, state, depth=3):
        """获取需要更新的相关状态"""
        relevant = set()
        queue = [(state, 0)]

        while queue:
            s, d = queue.pop(0)
            if s in relevant or d > depth:
                continue
            relevant.add(s)

            # 添加前驱状态
            for prev_s in self.model:
                for a in self.model[prev_s]:
                    for r, next_s in self.model[prev_s][a]:
                        if next_s == s:
                            queue.append((prev_s, d + 1))

        return relevant

    def local_value_iteration(self, states, iterations=5):
        """在相关状态上进行局部价值迭代"""
        for _ in range(iterations):
            for s in states:
                if not self.model[s]:  # 没有经验的状态
                    continue

                best_value = -float("inf")
                for a in self.model[s]:
                    # 基于经验估计Q值
                    total_value = 0
                    count = len(self.model[s][a])

                    for r, next_s in self.model[s][a]:
                        total_value += r + self.gamma * self.V[next_s]

                    expected_value = total_value / count if count > 0 else 0
                    best_value = max(best_value, expected_value)

                if best_value > -float("inf"):
                    self.V[s] = best_value

    def choose_action(self, state, epsilon=0.1):
        """选择动作"""
        if np.random.random() < epsilon or not self.model[state]:
            return np.random.randint(self.n_actions)

        best_action = None
        best_value = -float("inf")

        for a in range(self.n_actions):
            if a not in self.model[state]:
                continue

            total_value = 0
            count = len(self.model[state][a])

            for r, next_s in self.model[state][a]:
                total_value += r + self.gamma * self.V[next_s]

            expected_value = total_value / count
            if expected_value > best_value:
                best_value = expected_value
                best_action = a

        return (
            best_action
            if best_action is not None
            else np.random.randint(self.n_actions)
        )

    def take_action(self, s: State):
        if random.random() < self.epsilon or s.state not in self.model:
            return s.get_random_action()
        best_action, best_value = None, -inf
        for a in s.get_sort_actions():
            if a.action not in self.model[s.state]:
                continue
            total_value = self.model[s.state][a.action] + self.g
