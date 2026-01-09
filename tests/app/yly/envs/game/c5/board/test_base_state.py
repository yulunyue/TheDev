from app.yly.envs.game.c5.board.base_state import BoardC5State
from common.util.export import TestBase


class TestBaseState(TestBase):
    def setup_class(self):
        self.c = BoardC5State().load()
        return super().setup_class(self)

    def test_base(self):
        w, h = self.c.width - self.c.in_row + 1, self.c.height - self.c.in_row + 1
        self.expect(
            len(self.c.line_pos),
            2 * w * h + w * self.c.height + h * self.c.width,
            [v[0] for v in self.c.line_pos],
        )

    def test_put(self):
        self.c.set_pos_player_id(0, 2)
        self.expect(self.c.get_line_ct(), {-1: 3})
        self.c.set_pos_player_id(0, 1)
        self.expect(self.c.get_line_ct(), {1: 3})
        self.c.set_pos_player_id(1, 2)
        self.expect(self.c.get_line_ct(), {-1: 3, 1: 2})
