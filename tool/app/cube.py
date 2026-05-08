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

    def view_all(self):
        s = CubeState.new_shape(C.SHAPE2)
        self.dev_log.debug(s.show())
        for a in s.get_sort_actions():
            self.dev_log.debug(a.show())
            self.dev_log.debug(a.get_dst().show())

    def dev(self):
        self.view_all()


if __name__ == "__main__":
    CubeTool().run()
