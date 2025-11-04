from common.util.export import ToolBase, logger
from .state import State


class C5Tool(ToolBase):
    def test(self):
        s = State.new()
        logger.debug(s.show())
        for a in s.get_sort_actions():
            logger.debug(a.show())
            logger.debug(a.get_dst().show())


if __name__ == "__main__":
    C5Tool().run()
