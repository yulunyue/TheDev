from .env import PenduState
from common.util.export import ToolBase, logger
from common.algo.export import Dqn, Qlearning, np
from .constant import C


class ToolPen(ToolBase):

    def run_dqn(self):
        p = PenduState()
        dqn = Dqn().load(C.state_size, 128, 11, cache="data/game/pen/main.pt")
        dqn.search(p)

    def dev(self):
        s = PenduState()
        logger.info(s)


if __name__ == "__main__":
    ToolPen().run()
