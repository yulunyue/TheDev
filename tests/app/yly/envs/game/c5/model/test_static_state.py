from common.util.export import TestBase
from app.yly.envs.game.c5.model.static_state import StateStatic


class TestStaticState(TestBase):
    def test_state_3_3_3(self):
        s = StateStatic.set_board(3, 3, 3)
        actions = s.get_sort_actions()
        self.expect(len(actions), s.board.size)

        a = s.get_next(0, 1, 3, 4).get_action(6)
        s = a.get_dst()
        self.expect(s.done, s.FIRST_WIN, s.show())
        self.expect(a.reward, 1)
