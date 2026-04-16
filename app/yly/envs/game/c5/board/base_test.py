from common.util.export import List
from app.yly.envs.game.c5.board.base import BoardC5


class TestBase:
    def test_line_mask_head(self):
        b = BoardC5().load(5, 5, 3)
        assert [b.mask_format(v[0]) for v in b.lines[0]] == [
            "10000\nC0000\n10000\n10000\n00000",
            "10000\n10000\nC0000\n10000\n10000",
            "1C110\n00000\n00000\n00000\n00000",
            "10000\n0C000\n00100\n00010\n00000",
            "11C11\n00000\n00000\n00000\n00000",
            "10000\n01000\n00C00\n00010\n00001",
        ]

    def test_line_mask_mid(self):
        b = BoardC5().load(5, 5, 3)
        ln2 = b.lines[b.yx_to_idx(2, 2)]
        assert len(ln2) == 4 * 4
        assert [b.mask_format(v[0]) for v in ln2] == [
            "C0000\n01000\n00100\n00000\n00000",
            "00000\n00000\nC1100\n00000\n00000",
            "00000\n00000\n00100\n01000\nC0000",
            "10000\n0C000\n00100\n00010\n00000",
            "00000\n00000\n1C110\n00000\n00000",
            "00000\n00010\n00100\n0C000\n10000",
            "00C00\n00100\n00100\n00000\n00000",
            "00100\n00C00\n00100\n00100\n00000",
            "00000\n00100\n00100\n00C00\n00100",
            "00000\n00000\n00100\n00100\n00C00",
            "00001\n000C0\n00100\n01000\n00000",
            "00000\n00000\n011C1\n00000\n00000",
            "00000\n01000\n00100\n000C0\n00001",
            "0000C\n00010\n00100\n00000\n00000",
            "00000\n00000\n0011C\n00000\n00000",
            "00000\n00000\n00100\n00010\n0000C",
        ]

    def test_line_mask_tail(self):
        b = BoardC5().load(5, 5, 3)
        assert [b.mask_format(v[0]) for v in b.lines[-1]] == [
            "10000\n01000\n00C00\n00010\n00001",
            "00000\n00000\n00000\n00000\n11C11",
            "00000\n01000\n00100\n000C0\n00001",
            "00000\n00000\n00000\n00000\n011C1",
            "00001\n00001\n0000C\n00001\n00001",
            "00000\n00001\n00001\n0000C\n00001",
        ]

    def test_mask_formats(self):
        b = BoardC5().load(2, 2, 2)
        assert b.mask_formats(range(0, len(b.line_mask))) == [
            "C1\n00",
            "C0\n10",
            "C0\n01",
            "00\nC1",
            "10\nC0",
            "01\nC0",
            "1C\n00",
            "0C\n01",
            "0C\n10",
            "00\n1C",
            "01\n0C",
            "10\n0C",
        ]
        assert [b.foramt_line_state(v) for v in b.line_state] == [
            "#?-",
            "#?-",
            "#?-",
            "#?-",
            "-?#",
            "-?#",
            "-?#",
            "#?-",
            "#?-",
            "-?#",
            "-?#",
            "-?#",
        ]

    def test_get_next_states(self):
        b = BoardC5().load(2, 2, 2)
        next_states = b.get_next_states()
        assert next_states == [17, 34, 68, 136], [b.show(v) for v in next_states]

    def test_format(self):
        b = BoardC5().load(2, 2, 2)
        assert [b.mask_format(v[0]) for v in b.lines[0]] == [
            "10\nC0",
            "1C\n00",
            "10\n0C",
        ]

    def test_put_chess(self):
        b = BoardC5().load(2, 2, 2)
        b.put_chess(0, 1)
        assert [b.foramt_line_state(v) for v in b.line_state] == [], b.show()
        next_states = b.get_next_states()
        assert b.states_all_format() == {"O?#": 3}, b.show()
        assert next_states == [49, 81, 145]
