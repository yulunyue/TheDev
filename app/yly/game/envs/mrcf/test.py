from common.util.export import TestBase, logger
from .util import MdpAlgo
from .model.mrp_state import MrpState


class TestMain(TestBase):
    def test_mpr(self):
        s = MrpState.new(0)
        self.expect(s.get_actions_score([0, 1, 2, 5]), -2.5)


if __name__ == "__main__":
    TestMain().run()
