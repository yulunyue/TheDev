from common.util.export import TestBase, logger, Module
from common.algo.export import ALgoManage, Algo, State, random_seed
from common.third_util.export import CodingGame
from .util import Pm
from .model.ttstate import TtState, TtAction
from .constant import C, SC
from .cg import TicTocCg


class TestTicToc(TestBase):
    def test_cg(self, mode="submit"):
        Module().compile_one("app/yly/game/envs/tic_toc/cg.py")
        if mode == "submit":
            CodingGame("tc").pk(
                Module.RUN_TMP_PATH, TicTocCg.game_id, TicTocCg.agentsIds
            )
        elif mode == "replay":
            TicTocCg().replay()

    def test_actor(self):
        s = TtState.new_state(C.INIT_SATTE)
        ans = ALgoManage().set_init_state(s).actor([Pm.ab4, Pm.ab1], max_turn=101)
        logger.info(f"lose: {ans}")

    def test_search(self):
        s = TtState.new_state(C.INIT_SATTE)
        b: TtAction = Pm.ab1.search(s)
        logger.info(s)
        logger.info(b.dst)

    def test_fight(self):
        s = TtState.new_state(C.INIT_SATTE)
        ALgoManage().set_init_state(s).set_players(
            [Pm.ab1, Pm.ab2, Pm.ab3, Pm.ab4, Pm.rn]
        ).fight()

    def test_debug(self):
        self.test_dev4()

    def test_dev3(self):
        s = TtState.new_state(98)
        logger.info(s)

    def test_dev4(self):
        self.test_ec(Pm.bl1)

    def test_ec(self, algo: Algo):
        for k, v in C.get_except().items():
            a = algo.search(TtState.new_state(k))
            self.expect(a.action, v, a.src)

    def test_dev5(self):
        s = TtState.new_state(SC.SC1)
        Pm.bl1.search(s)
        logger.info(s.data["records"])


if __name__ == "__main__":
    random_seed(7)
    TestTicToc().run()
