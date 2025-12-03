from common.util.export import ToolBase, logger, Module, log
from .model import CubeState, C
from .algo import Al


class Solution(ToolBase):
    def random(self, step=10):
        s = CubeState.new_shape(C.SHAPE2)
        log.debug(s.show())
        for _ in range(step):
            a = s.get_random_action()
            log.debug(a.show())
            log.debug(a.get_dst().show())
        return s

    def view2(self):
        s = CubeState.new_shape(C.SHAPE2).random_step(10)
        logger.debug(s.show())
        actions = s.bfs()[C.init_mask][0]
        for a in actions:
            logger.debug(a.show())
            logger.debug(a.get_dst().show())

    def dev(self):
        self.random()


if __name__ == "__main__":
    Solution().run()
