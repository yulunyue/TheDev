from common.util.export import TestBase
from common.algo.export import random_seed
from app.yly.envs.game.c5.player.al import Al
from app.yly.envs.game.c5.model.dyn_state import StateStatic, DynState


def get_s_333_1():
    s = StateStatic.set_board(3, 3, 3)
    return s.get_next(0, 1, 3)


def get_s_333_2():
    s = DynState.set_board(3, 3, 3)
    return s.get_next(0, 1, 2, 3, 4, 5)


class TestAl(TestBase):

    def test_al333_ql(self):
        random_seed(1)
        s = get_s_333_2()
        self.expect(s.can_moves, [6, 7, 8])
        ql = Al().ql().set_train_epoll(4)
        ql.train(s)
        a = ql.search(s)
        self.expect(a.action, 6, s.show())
