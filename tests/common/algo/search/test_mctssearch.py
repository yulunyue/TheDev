from common.util.export import TestBase, logger
from common.algo.export import MctsSearch, DemoState


class TestMctssearch(TestBase):
    def test_search(self):
        s = DemoState.make_test_state()
        init_state = s.state
        al = MctsSearch().load(num_episodes=10)
        a = al.search(s)
        self.expect(s.state, init_state)
