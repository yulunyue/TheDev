from .model import Bandit
from common.util.export import ToolBase
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
        self.e = Bandit.new(10)
        self.d = Draw()

    def run_eg(self):
        self.run_algo(EpsilonGreedy().load(C.EG_EPSILION))

    def test_de(self):
        self.algo(DecayingEpsilonGreedy().load(epsilon=0.1))

    def test_ucb(self):
        self.algo(Ucb().load())

    def test_ts(self):
        self.algo(ThompsonSampling().load())

    def test_mcts(self):
        self.algo(MctsEasy().load())

    def debug(self):
        self.test_mcts()

    def main(self):

        self.d.draw_line(algo.rewards_record, title=algo.name)

    def run_algo(self, algo: EpsilonGreedy):
        algo.simulation(self.e)

    def exit(self):
        return self.d.save(self.get_temp_file(f"all.svg"))


if __name__ == "__main__":
    ToolBan().run()
