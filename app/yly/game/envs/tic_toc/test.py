from common.util.export import TestBase, logger
from common.algo.export import ALgoManage, Algo, State
from .util import Pm
from .model.ttstate import TtState
from .constant import C


def fight(p1: Algo, p2: Algo, state: State):
    ALgoManage().actor([p1, p2], state)


class TestTicToc(TestBase):
    def test_dev1(self):
        fight(Pm.ab, Pm.ab, TtState.new_state(C.INIT_SATTE))

    def test_dev2(self):
        a = TtState.new_state(C.INIT_SATTE)
        s = a.get_action(2 * 9 + 3)
        self.expect(False, True, s.dst)

    def test_debug(self):
        self.test_dev2()


if __name__ == "__main__":
    TestTicToc().run()
