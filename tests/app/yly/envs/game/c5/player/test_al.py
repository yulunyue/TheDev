from common.util.export import TestBase
from app.yly.envs.game.c5.player.al import Al
from app.yly.envs.game.c5.model.dyn_state import StateStatic, DynState


def get_s_333_1():
    s = StateStatic.set_board(3, 3, 3)
    return s.get_next(0, 1, 3)


def get_s_333_2():
    s = DynState.set_board(3, 3, 3)
    return s.get_next(0, 1, 2, 3, 4, 5)


class TestAl(TestBase):
    def test_al333_al(self):
        s = get_s_333_1()
        a = Al().ad(2).search(s)
        self.expect(a.action, 6, s.show())
        a = Al().mc().search(s)
        self.expect(a.action, 6, s.show())
        a = Al().ad(2).search(s.get_next(7))
        self.expect(a.action, 6)

    def test_al333_ql(self):
        s = get_s_333_2()
        ql = Al().ql(train_epoll=10)
        ql.train(s)
        # ql.search(s)
        # self.expect(a.action, 6, s.show())
