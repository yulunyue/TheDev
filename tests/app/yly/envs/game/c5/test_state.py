from common.util.export import TestBase
from app.yly.envs.game.c5.model.static_state import StateStatic


class TestState885(TestBase):
    def setup_class(self):

        return super().setup_class(self)


class TestState(TestBase):
    def setup_class(self):

        return super().setup_class(self)

    def test_view1(self):
        s = StateStatic.new(295581378981694412433)
        self.expect(s.done, StateStatic.SECONEND_WIN)
