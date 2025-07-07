from common.util.export import TestBase, logger, Module
from common.algo.export import ALgoManage, Algo, State, random_seed
from common.third_util.export import CodingGame
from .util import Pm
from .model.ttstate import TtState
from .constant import C
from .cg import TicTocCg


class TestTicToc(TestBase):
    def test_cg(self, mode="submit"):
        Module().compile_one("app/yly/game/envs/l9/cg.py")
        if mode == "submit":
            CodingGame("cf4").pk(
                Module.RUN_TMP_PATH, TicTocCg.game_id, TicTocCg.agentsIds
            )
        elif mode == "replay":
            TicTocCg().replay()

    def test_actor(self):
        s = TtState.new_state(C.INIT_SATTE)
        ans = ALgoManage().actor([Pm.ab1, Pm.ab1], s, max_turn=100)
        logger.info(f"lose:{ans}")

    def test_fight(self):
        s = TtState.new_state(C.INIT_SATTE)
        ALgoManage().fight([Pm.ab1, Pm.ab2, Pm.ab3, Pm.ab4], s)

    def test_debug(self):
        self.test_actor()

    def test_dev3(self):
        s = TtState.new_state(98)
        logger.info(s)


if __name__ == "__main__":
    random_seed(7)
    TestTicToc().run()
