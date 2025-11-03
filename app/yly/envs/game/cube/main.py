from common.util.export import ToolBase, logger, Module
from .model import CubeState


class Solution(ToolBase):
    def view(self):
        s = CubeState.new_shape(2)
        logger.debug(s.show())

    def debug(self):
        self.view()


if __name__ == "__main__":
    Solution().run()
