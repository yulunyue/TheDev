from common.util.export import List
from app.yly.envs.game.c5.board.base import BoardC5


class TestBase:
    def test_line_mask(self):
        b = BoardC5().load(5, 5, 3)
        assert [b.mask_format(b.line_mask[v]) for v in b.lines[0]] == [
            "11100\n00000\n00000\n00000\n00000",
            "10000\n10000\n10000\n00000\n00000",
            "10000\n01000\n00100\n00000\n00000",
        ]
        assert [b.mask_format(b.line_mask[v]) for v in b.lines[b.yx_to_idx(2, 2)]] == [
            "10000\n01000\n00100\n00000\n00000",
            "00000\n00000\n11100\n00000\n00000",
            "00000\n01000\n00100\n00010\n00000",
            "00000\n00000\n01110\n00000\n00000",
            "00100\n00100\n00100\n00000\n00000",
            "00000\n00100\n00100\n00100\n00000",
            "00000\n00000\n00111\n00000\n00000",
            "00000\n00000\n00100\n00100\n00100",
            "00000\n00000\n00100\n00010\n00001",
            "00000\n00000\n00100\n01000\n10000",
            "00000\n00010\n00100\n01000\n00000",
            "00001\n00010\n00100\n00000\n00000",
        ]

        assert [b.mask_format(b.line_mask[v]) for v in b.lines[-1]] == [
            "00000\n00000\n00100\n00010\n00001",
            "00000\n00000\n00000\n00000\n00111",
            "00000\n00000\n00001\n00001\n00001",
        ]

    def test_get_next_state(self):
        b = BoardC5().load(2, 2, 2)
        next_states = b.get_next_states()
        view = BoardC5().load(2, 2, 2)
        assert next_states == [17, 34, 68, 136], [
            view.set_state(v).to_str() for v in next_states
        ]

        b.put_chess(0, 1)
        next_states = b.get_next_states()
        assert next_states == [49, 81, 145], [
            view.set_state(v).to_str() for v in next_states
        ]
