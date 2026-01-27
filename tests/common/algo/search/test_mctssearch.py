from common.util.export import TestBase, logger
from common.algo.export import random_seed
from common.algo.export import MctsSearch, DemoState

S2 = [""] * 32
S2 += [
    """---
: done=False n=33 q=0 u=inf
  a=0 r=1: done=True n=16 q=1.000 u=0.652
  a=1: done=False n=8 q=0.625 u=0.921
    a=0 r=1: done=True n=5 q=1.000 u=0.873
    a=1 r=0: done=True n=2 q=0.000 u=1.953
  a=2: done=False n=9 q=0.667 u=0.921
    a=0 r=0: done=True n=2 q=0.000 u=2.019
    a=1 r=1: done=True n=5 q=1.000 u=0.903
    a=2 r=0: done=True n=1 q=0.000 u=2.019
---"""
]


class TestMctssearch(TestBase):
    @classmethod
    def setup_class(cls):
        random_seed(0)

    def test_search(self):
        s = DemoState.make_test_state().load_mcts(None)
        al = MctsSearch().load(num_episodes=10)

        for e in S2:
            al.search_one_round(s)
            if e:
                self.expect(s.print_tree(), e)
