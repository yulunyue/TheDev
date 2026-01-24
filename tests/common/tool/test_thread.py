from common.tool.thread_util import ThreadRecord
from common.util.export import TestBase


class RcCls(ThreadRecord):
    def init(self):
        self.a = 0
        self.b = 0

    def exec_main(self):
        for _ in range(3):
            self.a += 1
            self.b += 1
        return self.a

    def uk(self):
        return f"{self.a}"

    def to_josn(self):
        return dict(a=self.a, b=self.b)


class TestThread(TestBase):
    def test_rc(self):
        s = RcCls().execute()
        self.expect(s.result, 3)
        self.expect(
            s.records,
            [{"a": 0, "b": 0}, {"a": 1, "b": 0}, {"a": 2, "b": 1}, {"a": 3, "b": 2}],
        )


if __name__ == "__main__":
    TestThread().run()
