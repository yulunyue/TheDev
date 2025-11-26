from common.util.export import ToolBase, logger, random

from .model.mrp_state import MrpState, computer, C1
from .model.mdp_state import MdpState


class Main(ToolBase):
    def dev1(self):
        s = MrpState().new(0)
        r = s.get_reward_by_actions([1, 2, 3, 6], gamma=0.5)
        logger.info(r)
        logger.info(computer(C1.MRP_REWARD, C1.MRP_P))

    def dev(self):
        self.dev1()


if __name__ == "__main__":
    Main().run()
