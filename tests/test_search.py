from common.util.export import TestBase, logger
from common.algo.export import TestState, AbDev, Algo, MctsSearch


class TestSearch(TestBase):
    def prepare(self, args=None):
        self.s = TestState.make_test_state()
        self.al1 = AbDev("dfs").load(10).set_record_dir("data/test/search")
        self.al2 = (
            AbDev("ab1").load(10, AbDev.AB_TYPE).set_record_dir("data/test/search")
        )
        self.al3 = (
            AbDev("abm").load(10, AbDev.AB_MUCH).set_record_dir("data/test/search")
        )
        self.ms1 = MctsSearch("ms1").load()
        logger.debug(self.s.dump_tree())

    def check_algo(self, a: Algo):
        state_num = 0
        for actions, s1 in self.s.bfs().values():
            if s1.get_done() is not None or s1.max_reward is None:
                continue
            s: TestState = s1
            a.search(s)
            self.expect(a.get_state_reward(s), s.max_reward, s.show(title=a.get_name()))
            state_num += a.state_num
        logger.debug([a.get_name(), state_num])

    def test_easy(self):
        self.check_algo(self.al1)
        self.check_algo(self.al2)
        self.check_algo(self.al3)
        self.check_algo(self.ms1)

    # def test_much(self):
    #     s = TestState.make_test_state(5, 7)
    #     AbDev("dfs").load(6).search(s)

    def debug(self):
        # c = self.al3.search(self.s.get_dst([1]))
        # logger.info(c.action)
        self.check_algo(self.al3)


if __name__ == "__main__":
    TestSearch().run()
