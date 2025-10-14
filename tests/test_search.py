from common.util.export import TestBase, logger
from common.algo.export import TestState, AbDev, Algo, MctsSearch, ALgoManage
from common.tool.export import ThreadRecord


class Record(ThreadRecord):
    def __init__(self, s: TestState):
        self.s = s
        super().__init__()

    def uk(self):
        return self.s.print_tree()

    def set_search(self, algo: Algo):
        return self.set_exec(lambda *args: algo.search(self.s))


class TestSearch(TestBase):
    def prepare(self, args=None):
        self.s = TestState.make_test_state()
        self.al = ALgoManage().set_record_dir("data/test/search")
        logger.debug(self.s.print_tree())

    def check_algo(self, a: Algo):
        ac = a.search(self.s)
        logger.debug(ac.get_dst().state)

    def dev(self):
        self.check_algo(self.al.ab())

    def cli(self):
        Record(self.s).set_search(self.al.mc()).cli()

    def debug(self):
        self.dev()


if __name__ == "__main__":
    TestSearch().run()
