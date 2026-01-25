from common.util.export import TestBase, logger
from common.algo.export import random_seed
from common.algo.export import MctsSearch, DemoState

S2 = [
    """---
: depth=0 done=False n=1 q=-1.0 u=0
  a=0 r=1: depth=0 done=False n=1 q=1.0 u=0.0
  a=1 r=0: depth=0 done=False n=0 q=0 u=0.0
    a=0 r=None: TODO
    a=1 r=None: TODO
  a=2 r=0: depth=0 done=False n=0 q=0 u=0.0
    a=0 r=None: TODO
    a=1 r=None: TODO
    a=2 r=None: TODO
---""",
    """""",
]


class TestMctssearch(TestBase):
    @classmethod
    def setup_class(cls):
        random_seed(0)

    def test_search(self):
        s = DemoState.make_test_state()
        al = MctsSearch().load(num_episodes=10)
        for e in S2:
            al.search_one_round(s)
            self.expect(s.print_tree(), e)
