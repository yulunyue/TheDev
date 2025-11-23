from common.util.export import ToolBase, logger, Module
from .model import CubeState, C
from .algo import Al


class Solution(ToolBase):
    def view1(self):
        s = CubeState.new_shape(C.SHAPE2)
        logger.debug(s.show())
        logger.debug(len(s.get_sort_actions()))
        for a in s.get_sort_actions():
            logger.debug(a.show())
            logger.debug(a.get_dst().show())

    def view2(self):
        s = CubeState.new_shape(C.SHAPE2).random_step(10)
        logger.debug(s.show())
        actions = s.bfs()[C.init_mask][0]
        for a in actions:
            logger.debug(a.show())
            logger.debug(a.get_dst().show())

    def dev(self):
        self.view1()


if __name__ == "__main__":
    Solution().run()
