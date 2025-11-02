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
    """python -m tests.mrcf_test debug"""

    def dev(self):
        pass


if __name__ == "__main__":
    Main().run()
