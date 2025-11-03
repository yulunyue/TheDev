from common.util.export import ToolBase, logger, Module
from .model import CubeState, C


class Solution(ToolBase):
    def view(self):
        s = CubeState.new_shape(C.SHAPE2)
        logger.debug(s.show())
        for a in s.get_sort_actions():
            logger.debug(a.show())
            logger.debug(a.get_dst().show())

    def debug(self):
        self.view()


if __name__ == "__main__":
    Solution().run()
