from common.util.export import TestBase, logger
from common.algo.search.states.demo_state import DemoState

S1 = """---
: depth=0 done=False
  a=0 r=None: TODO
  a=1 r=None: TODO
  a=2 r=None: TODO
---"""

S2 = """---
: depth=0 done=False
  a=0 r=None: TODO
  a=1 r=0: depth=0 done=False
    a=0 r=None: TODO
    a=1 r=None: TODO
  a=2 r=None: TODO
---"""


class TestDemoState(TestBase):
    def test_base(self):
        s = DemoState.make_test_state()
        self.expect(s.print_tree(), S1)
        s.get_action(1).do()
        self.expect(s.print_tree(), S2)
