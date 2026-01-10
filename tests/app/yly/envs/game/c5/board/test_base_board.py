from app.yly.envs.game.c5.board.base import BoardC5
from common.util.export import TestBase


class TestBaseBoard(TestBase):
    @classmethod
    def setup_class(cls):
        cls.c = BoardC5().load()
        return super().setup_class()

    def test_put_chess(self):
        ct = TestBaseBoard.c.put_chess(0, 1)
        self.expect(ct, {(1, 1): 3})
        ct = TestBaseBoard.c.put_chess(1, 1)
        self.expect(ct, {(1, 1): 2, (2, 1): 1})
        ct = TestBaseBoard.c.put_chess(2, 1)
        self.expect(ct, {(1, 1): 2, (3, 1): 1})
        TestBaseBoard.c.change_chess_statu(2, 0)

        ct = TestBaseBoard.c.put_chess(3, 1)
        self.expect(ct, {(1, 1): 2, (3, 1): 1})
        TestBaseBoard.c.change_chess_statu(3, 0)

        ct = TestBaseBoard.c.put_chess(4, 1)
        self.expect(ct, {(1, 1): 2, (2, 1): 1})
        TestBaseBoard.c.change_chess_statu(4, 0)

        ct = TestBaseBoard.c.put_chess(5, 1)
        self.expect(ct, {(1, 1): 3})
