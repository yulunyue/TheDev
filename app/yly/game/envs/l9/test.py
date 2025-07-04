from common.util.export import TestBase, Module, logger
from common.third_util.export import CodingGame
from common.algo.export import Algo, AlphaBateSearch, ALgoManage
from .cg import Cgl9
from .api import L9Api, ApiAlgo
from .model.l9state import L9State, L9Action
from .shape.env import L9ENV, C
from .util import get_player, PM


class TestL9(TestBase):
    def test_cg(self, mode="submit"):
        Module().compile_one("app/yly/game/envs/l9/cg.py")
        if mode == "submit":
            CodingGame("cf4").pk(Module.RUN_TMP_PATH, Cgl9.game_id, Cgl9.agentsIds)
        elif mode == "replay":
            Cgl9().replay()

    def test_dev1(self):
        self.test_algo(L9Api())

    def test_dev2(self):
        self.test_pk(PM.api, PM.api, L9State.new_state(C.INIT_STATE))

    def test_dev3(self):
        s = L9State.new_state(C.INIT_STATE)
        self.expect(s.place_move, C.PLACES_MAX_TURN, s)
        a1 = s.get_action("PLACE;A1")
        self.expect(a1.dst.place_move, C.PLACES_MAX_TURN - 1, a1.dst)
        a2 = a1.dst.get_action("PLACE;A4")
        self.expect(a2.dst.place_move, C.PLACES_MAX_TURN - 2, a2.dst)

    def test_dev4(self):
        s = L9State.new_state(C.INIT_STATE)
        s = s.get_action("PLACE;A1").dst
        logger.info(s)

    def test_dev5(self):
        s=L9State.new_state(2500898089577)
        logger.info(s)

    def test_debug(self):
        self.test_dev5()

    def test_algo(self, algo: Algo):
        for k, v in C.get_excepts().items():
            s = L9State.new_state(k)
            a: L9Action = algo.search(s)
            self.expect(a.action, v, f"algo:{algo.get_name()},s:{s}")

    def test_pk(self, algo1: Algo, algo2: Algo, s: L9State):
        ans=ALgoManage().actor([get_player(algo1), get_player(algo2)], s, max_turn=200)
        logger.info(ans)
    def exit(self):
        L9Api.new().cache.flush()


if __name__ == "__main__":
    TestL9().run()
