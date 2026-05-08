from common.util.export import logger, Module, log
from common.tool.export import ToolBase
from common.algo.export import random_seed
from app.yly.envs.game.cube.model import CubeState, C
from app.yly.envs.game.cube.algo import Al


class CubeTool(ToolBase):

    def random(self, step=10):
        random_seed()
        s = CubeState.new_shape(C.SHAPE2)
        log.debug(s.show())
        for _ in range(step):
            a = s.get_random_action()
            log.debug(a.show())
            log.debug(a.get_dst().show())
        return s


if __name__ == "__main__":
    CubeTool().run()
