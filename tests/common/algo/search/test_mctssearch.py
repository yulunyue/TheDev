from common.util.export import TestBase, logger
from common.algo.export import random_seed
from common.algo.export import MctsSearch, DemoState

S2 = (
    [
        """---
: done=False n=1 q=0 u=inf
  a=0: done=True
  a=1: done=False n=1 q=0.000 u=inf
    a=0: done=True
    a=1 r=0: done=True
  a=2: done=False
    a=0: done=True
    a=1: done=True
    a=2: done=True
---""",
        """---
: done=False n=2 q=0 u=inf
  a=0 r=1: done=True n=1 q=1.000 u=inf
  a=1: done=False n=1 q=0.000 u=0.000
    a=0: done=True
    a=1 r=0: done=True
  a=2: done=False
    a=0: done=True
    a=1: done=True
    a=2: done=True
---""",
        """---
: done=False n=3 q=0 u=inf
  a=0 r=1: done=True n=1 q=1.000 u=1.166
  a=1: done=False n=1 q=0.000 u=1.166
    a=0: done=True
    a=1 r=0: done=True
  a=2: done=False n=1 q=1.000 u=inf
    a=0: done=True
    a=1 r=1: done=True
    a=2: done=True
---""",
        """---
: done=False n=4 q=0 u=inf
  a=0 r=1: done=True n=1 q=1.000 u=1.467
  a=1: done=False n=1 q=0.000 u=1.467
    a=0: done=True
    a=1 r=0: done=True
  a=2: done=False n=2 q=1.000 u=1.467
    a=0: done=True
    a=1 r=1: done=True n=1 q=1.000 u=inf
    a=2: done=True
---""",
        """---
: done=False n=5 q=0 u=inf
  a=0 r=1: done=True n=2 q=1.000 u=1.648
  a=1: done=False n=1 q=0.000 u=1.648
    a=0: done=True
    a=1 r=0: done=True
  a=2: done=False n=2 q=1.000 u=1.166
    a=0: done=True
    a=1 r=1: done=True n=1 q=1.000 u=inf
    a=2: done=True
---""",
    ]
    + [""] * 32
    + ["""---
: done=False n=38 q=0 u=inf
  a=0 r=1: done=True n=21 q=1.000 u=0.595
  a=1: done=False n=8 q=0.625 u=0.941
    a=0 r=1: done=True n=5 q=1.000 u=0.873
    a=1 r=0: done=True n=2 q=0.000 u=1.953
  a=2: done=False n=9 q=0.667 u=0.887
    a=0 r=0: done=True n=2 q=0.000 u=2.019
    a=1 r=1: done=True n=5 q=1.000 u=0.903
    a=2 r=0: done=True n=1 q=0.000 u=2.019
---"""]
)


class TestMctssearch(TestBase):

    def test_search(self):
        random_seed(0)
        s = DemoState.make_test_state().load_mcts(None)
        al = MctsSearch().load(num_episodes=10)

        for i, e in enumerate(S2):

            al.search_one_round(s)
            if e:
                self.expect(s.print_tree(), e)
