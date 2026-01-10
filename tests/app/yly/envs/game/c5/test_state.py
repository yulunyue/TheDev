from common.util.export import TestBase
from app.yly.envs.game.c5.state import State


class TestState885(TestBase):
    def setup_class(self):

        return super().setup_class(self)


class TestState(TestBase):
    def setup_class(self):

        return super().setup_class(self)

    def test_view1(self):
        s = State.new(295581378981694412433)
        self.expect(s.done, State.SECONEND_WIN)
