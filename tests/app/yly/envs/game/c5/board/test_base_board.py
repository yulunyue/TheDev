from app.yly.envs.game.c5.board.base import BoardC5
from common.util.export import TestBase


class TestBaseBoard(TestBase):

    def test_put_chess(self):
        c = BoardC5().load()
        ct = c.put_chess(0, 1)
        self.expect(ct, {(1, 1): 3})
        ct = c.put_chess(1, 1)
        self.expect(ct, {(1, 1): 2, (2, 1): 1})
        ct = c.put_chess(2, 1)
        self.expect(ct, {(1, 1): 2, (3, 1): 1})
        c.change_chess_statu(2, 0)

        ct = c.put_chess(3, 1)
        self.expect(ct, {(1, 1): 2, (3, 1): 1})
        c.change_chess_statu(3, 0)

        ct = c.put_chess(4, 1)
        self.expect(ct, {(1, 1): 2, (2, 1): 1})
        c.change_chess_statu(4, 0)

        ct = c.put_chess(5, 1)
        self.expect(ct, {(1, 1): 3})
