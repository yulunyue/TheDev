from common.util.export import TestBase, logger
from common.algo.export import TestState, AbDev, Algo, MctsSearch


class TestSearch(TestBase):
    def prepare(self, args=None):
        self.s = TestState.make_test_state()
        self.al1 = AbDev("dfs").load(10)
        self.al2 = AbDev("ab1").load(10, AbDev.AB_TYPE)
        self.al3 = AbDev("abm").load(10, AbDev.AB_MUCH)
        self.ms1 = MctsSearch("ms1").load()
        logger.debug(self.s.dump_tree())

    def check_algo(self, a: Algo):
        b = a.search(self.s.get_dst([0, 0]))
        self.expect(b.action, 0)
        b = a.search(self.s.get_dst([0]))  # 2
        self.expect(b.action, 0)
        b = a.search(self.s.get_dst([1]))  # 3
        self.expect(b.action, 0)
        b = a.search(self.s.get_dst([2]))  # 4
        self.expect(b.action, 0)
        b = a.search(self.s)
        self.expect(b.action, 2)
        logger.info(f"{a.name}->state_num:{a.state_num}")

    def test_easy(self):
        self.check_algo(self.al1)
        self.check_algo(self.al2)
        self.check_algo(self.al3)
        self.check_algo(self.ms1)

    def test_much(self):
        s = TestState.make_test_state(5, 7)
        AbDev("dfs").load(6).search(s)

    def debug(self):
        self.test_abdfs()


if __name__ == "__main__":
    TestSearch().run()
