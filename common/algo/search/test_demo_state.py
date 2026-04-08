from common.util.export import TestBase, logger
from common.algo.search.states.demo_state import DemoState

S1 = """---
: done=False
  a=0: done=True
  a=1: done=False
    a=0: done=True
    a=1: done=True
  a=2: done=False
    a=0: done=True
    a=1: done=True
    a=2: done=True
---"""

S2 = """---
: done=False
  a=0 r=1: done=True
  a=1: done=False
    a=0: done=True
    a=1: done=True
  a=2: done=False
    a=0: done=True
    a=1: done=True
    a=2: done=True
---"""


class TestDemoState(TestBase):
    def test_base(self):
        s = DemoState.make_test_state()
        self.expect(s.print_tree(), S1)
        s.get_action(0).do()
        self.expect(s.print_tree(), S2)
