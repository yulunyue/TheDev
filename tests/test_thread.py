from common.tool.thread_util import TestRc
from common.util.export import TestBase


class TestThread(TestBase):
    def test_rc(self):
        s = TestRc().execute()
        self.expect(s.result, 3)
        self.expect(
            s.records,
            [{"a": 0, "b": 0}, {"a": 1, "b": 0}, {"a": 2, "b": 1}, {"a": 3, "b": 2}],
        )

    def run_rc(self):
        TestRc().cli("data/log/view.txt")

    def debug(self):
        self.run_rc()


if __name__ == "__main__":
    TestThread().run()
