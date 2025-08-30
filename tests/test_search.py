from common.util.export import TestBase, logger
from common.algo.export import TestState, AbDev, Algo


class TestSearch(TestBase):
    def prepare(self, args=None):
        self.s = TestState.make_test_state()
        logger.debug(self.s.dump_tree())

    def check_algo(self, a: Algo):
        a.search(self.s)
        dst = self.s.get_best_actions()[-1].dst
        self.expect(dst.get_reward(), 11)

    def debug(self):
        self.test_abdfs()


if __name__ == "__main__":
    TestSearch().run()
