from common.algo.search.algo import Algo, Action, State

from common.util.export import logger, defaultdict, ListUtil, File
from common.third_util.np_util import np
from typing import List


class PolicyIteration(Algo):
    def set_pi(self, pi):
        self.pi: dict = pi
        return self

    def load(self, train_epoll=100, num_episodes=1000, theta=0.001, gamma=0.9):
        self.theta = theta
        self.gamma = gamma
        self.train_epoll = train_epoll
        self.num_episodes = num_episodes
        self.log_dir = (
            File(f"data/log/cf_walk/{self.get_name()}")
            .remove()
            .make_dir_if_not_exist(True)
        )
        logger.info(self.log_dir)
        return super().load()

    def reset(self):
        self.v = defaultdict(int)
        return super().reset()

    def search(self, state, *args, last_a=None, **kw) -> Action:
        return ListUtil(state.get_sort_actions()).max(self.get_action_value)[1]

    def get_action_value(self, action: Action):
        return action.get_reward() + self.gamma * self.v[action.get_dst().state]

    def get_qsa_value(self, qsalst):
        return sum(qsalst)

    def policy_evaluation(self, epool_num, states: List[State]):
        p_cnt = 0
        while self.num_episodes < 0 or p_cnt < self.num_episodes:
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
            p_cnt += 1
            self.log_value(new_values, max_diff, epool_num, p_cnt)
            if max_diff < self.theta:
                break

    def policy_improvement(self, cnt, states: List[State]):  # 策略提升
        pi = self.pi.copy()
        for s in states:
            spi = {a.action: self.get_action_value(a) for a in s.get_sort_actions()}
            if not spi:
                continue
            maxq = max(spi.values())
            cntq = sum(1 if v == maxq else 0 for v in spi.values())
            pi[s.state] = {k: 1 / cntq if spi[k] == maxq else 0 for k in spi}
        self.log_policy(pi, cnt)
        return pi

    def train(self, state: State):
        cnt = 0
        states = state.bfs()
        while cnt < self.train_epoll:
            self.policy_evaluation(cnt, states)
            pi = self.policy_improvement(cnt, states)
            cnt += 1
            if self.pi and self.pi == pi:
                break
            self.pi = pi
        return

    def log_value(self, v, diff, cnt, epoll_num):
        self.log_dir.child(f"value_{epoll_num}_{cnt}.json").write_file(
            dict(diff=diff, v=v)
        )

    def log_policy(self, pi, cnt):
        logger.info(self.log_dir.child(f"policy_{cnt}.json").write_file(pi))
