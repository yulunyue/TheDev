from common.util.export import TestBase, Module
from common.third_util.export import CodingGame
from common.algo.export import Algo, AlphaBateSearch
from .cg import Cgl9
from .api import L9Api
from .model.l9state import L9State, L9Action
from .shape.env import L9ENV, C


class TestL9(TestBase):
    def test_cg(self, mode="submit"):
        Module().compile_one("app/yly/game/envs/l9/cg.py")
        if mode == "submit":
            CodingGame("cf4").pk(Module.RUN_TMP_PATH, Cgl9.game_id, Cgl9.agentsIds)
        elif mode == "replay":
            Cgl9().replay()

    def test_1(self):
        self.test_algo(L9Api())

    def test_debug(self):
        self.test_algo(AlphaBateSearch().load(max_depth=1))

    def test_dev(self):
        pass

    def test_algo(self, algo: Algo):
        for k, v in C.get_excepts().items():
            s = L9State.new_state(k)
            a: L9Action = algo.search(s)
            self.expect(a.action, v, f"algo:{algo.get_name()},s:{s}")


if __name__ == "__main__":
    TestL9().run()
