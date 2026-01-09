from app.yly.envs.game.c5.board.base import BoardC5
from common.util.export import TestBase


class TestBase(TestBase):
    def setup_class(self):
        self.c = BoardC5().load()
        return super().setup_class(self)
