from app.yly.envs.game.c5.board.base_state import BoardC5State
from common.util.export import TestBase


class TestBaseState(TestBase):
    def setup_class(self):
        self.c = BoardC5State().load(6, 6, 4)
        return super().setup_class(self)

    def test_base(self):
        self.expect(len(self.c.line_pos), 120, self.c.line_pos)

    def test_put(self):
        self.c.set_pos_player_id(0, 2)
        self.expect(self.c.get_line_ct(), {-1: 3})
        self.c.set_pos_player_id(0, 1)
        self.expect(self.c.get_line_ct(), {1: 3})
        self.c.set_pos_player_id(1, 2)
        self.expect(self.c.get_line_ct(), {-1: 3, 1: 2})
