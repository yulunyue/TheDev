from common.util.export import TestBase
from app.yly.envs.game.c5.player.al import Al
from app.yly.envs.game.c5.model.static_state import StateStatic


class TestAl(TestBase):
    def test_al3_3_3(self):
        s = StateStatic.set_board(3, 3, 3)
        s = s.get_next(0, 1, 3)
        a = Al().ad(2).search(s)
        self.expect(a.action, 2, s.show())
