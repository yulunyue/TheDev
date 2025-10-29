from common.util.export import ToolBase, Module, logger
from common.third_service.export import CodingGame
from .cg import Cgl9
from .api import L9Api, ApiAlgo
from .model.l9state import L9State, L9Action
from .shape.env import L9ENV, C


class L9Tool(ToolBase):
    def prepare(self, args=None):
        Module().compile_one(Cgl9.main_py())

    def cg(self):
        CodingGame(Cgl9.name).pk(Module.RUN_TMP_PATH, Cgl9.game_id, Cgl9.agentsIds)


if __name__ == "__main__":
    L9Tool().run()
