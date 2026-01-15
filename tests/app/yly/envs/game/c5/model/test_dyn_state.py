from common.util.export import TestBase
from app.yly.envs.game.c5.model.dyn_state import DynState


class TestDynState(TestBase):
    def test_base(self):
        s: DynState = DynState.set_board(3, 3, 3)
        s = s.get_next(0, 1).get_action(2)
        self.expect(s.key, "0|1|2")
