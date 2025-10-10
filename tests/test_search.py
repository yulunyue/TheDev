from common.util.export import TestBase, logger
from common.algo.export import TestState, AbDev, Algo, MctsSearch, ALgoManage


class TestSearch(TestBase):
    def prepare(self, args=None):
        self.s = TestState.make_test_state()
        self.al = ALgoManage().set_record_dir("data/test/search")
        logger.debug(self.s.print_tree())

    def check_algo(self, a: Algo):
        ac = a.search(self.s)
        logger.debug(ac.get_dst().state)

    def test_easy(self):
        self.check_algo(self.al1)
        self.check_algo(self.al2)
        self.check_algo(self.al3)
        self.check_algo(self.ms1)

    def dev(self):
        self.check_algo(self.al.ab())

    def debug(self):
        # c = self.al3.search(self.s.get_dst([1]))
        # logger.info(c.action)
        # self.check_algo(self.al3)
        pass


if __name__ == "__main__":
    TestSearch().run()
