from common.util.export import ToolBase, logger, random
from common.algo.export import (
    MctsEasy,
    PolicyIteration,
    ValueIteration,
    AlphaBateSearch,
)
from .model.mrp_state import MrpState
from .model.mdp_state import MdpState


class Main(ToolBase):
    def dev1(self):
        s = MrpState().new(0)
        r = s.get_reward_by_actions([1, 2, 3, 6], gamma=0.5)
        logger.info(r)

    def dev(self):
        self.dev1()


if __name__ == "__main__":
    Main().run()
