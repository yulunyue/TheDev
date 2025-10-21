from common.algo.export import Algo
from ..model import Bandit, Action


class BaseAlgo(Algo):
    def simulation(self, s: Bandit, epolls):
        ret = 0
        record = []
        for _ in range(epolls):
            a = self.take_action(s)
            self.update_action(a)
            regret = s.get_regret(a.action)
            ret += regret
            record.append(ret)
        return record
