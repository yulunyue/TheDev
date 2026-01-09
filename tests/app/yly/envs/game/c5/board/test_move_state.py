from app.yly.envs.game.c5.board.base_move import BoardMove
from common.util.export import TestBase


class TestMoveState(TestBase):
    def setup_class(self):
        self.c = BoardMove().load()
        return super().setup_class(self)

    def test_put(self):
        self.c.set_pos_player_id(0, 1)
        self.c.set_pos_player_id(1, 1)
        self.expect(self.c.get_line_ct(), {-1: 3, 1: 2})
