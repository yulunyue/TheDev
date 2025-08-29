from common.algo.export import AbDev, Algo, MctsSearch
from .model.state_dev import Rooms


class Pm:

    def all(self):
        ret = []
        for i in range(1, 6):
            ret.append(self.ab(i))
        return ret

    def ab(self, depath, params=None):
        if params is None:
            params = [1]
        return (
            AbDev(f"ab{depath}").load(depath, AbDev.AB_TYPE)
        )

    def bl(self, depath, params=None):
        if params is None:
            params = [1]
        return AbDev(f"bl{depath}").load(depath)

    def mc(self):
        return MctsSearch("mc").load(max_depath=20, num_episodes=1000)


PM = Pm()
