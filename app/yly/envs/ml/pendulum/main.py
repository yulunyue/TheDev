from .env import PenduState, QNet
from common.util.export import ToolBase, logger
from .algo import DoubleDqn
from .constant import C
from ..cart_pole.main import CartTool


class ToolPen(CartTool):
    def get_init_state(self):
        return PenduState()

    def get_moudle_cls(self):
        return QNet

    def debug(self):
        self.dev()


if __name__ == "__main__":
    ToolPen().run()
