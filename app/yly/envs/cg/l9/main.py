from common.third_service.get_service import CodingGame
from common.util.export import ToolBase
from .cg import Cgl9
from .api import L9Api, ApiAlgo
from .model.l9state import L9State, L9Action
from .shape.env import L9ENV, C


class L9Tool(ToolBase):
    pass


if __name__ == "__main__":
    L9Tool().run()
