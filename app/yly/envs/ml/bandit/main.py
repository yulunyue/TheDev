from .model import Bandit
from common.util.export import ToolBase, logger
from common.third_util.draw import Draw
from .algo.eg import EpsilonGreedy
from .algo.deg import DecayingEpsilonGreedy
from .algo.tms import ThompsonSampling
from .algo.ucb import Ucb
from .constant import C

"""
多臂老虎机是一个
"""


class ToolBan(ToolBase):
    def prepare(self):
        self.s = Bandit.new(C.K)
        self.d = Draw()

    def run_eg(self):
        self.run_algo(EpsilonGreedy().load(C.EG_EPSILION1).set_name("eg1"))
        self.run_algo(EpsilonGreedy().load(C.EG_EPSILION2).set_name("eg3"))

    def run_de(self):
        self.run_algo(DecayingEpsilonGreedy().load(C.DE_EPSILION).set_name("de"))

    def run_ucb(self):
        self.run_algo(Ucb().load(C.COEF).set_name("ucb"))

    def debug(self):
        self.test_mcts()

    def main(self):
        self.run_eg()
        self.run_de()
        self.run_ucb()

    def run_algo(self, algo: EpsilonGreedy):
        result = algo.search(self.s, C.EPOLLS)
        self.d.draw_line(result, title=algo.get_name())
        logger.debug(f"\n{algo.show()}\n{self.s.show()}")

    def exit(self):
        path = self.get_temp_file(f"all.svg")
        return self.d.save(path)


if __name__ == "__main__":
    ToolBan().run()
