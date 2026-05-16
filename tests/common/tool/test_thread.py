from common.util.thread.thread_util import ThreadRecord
from common.util.export import TestBase


class RcCls(ThreadRecord):
    def init(self):
        self.ins = self
        self.a = 0
        self.b = 0
        self._layout_keys = ["a", "b"]
        self._last_state = {"a": 0, "b": 0}
        self.records = []

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
            [
                {"key": "a", "value": 1},
                {"key": "b", "value": 1},
                {"key": "a", "value": 2},
                {"key": "b", "value": 2},
                {"key": "a", "value": 3},
                {"key": "b", "value": 3},
            ],
        )


if __name__ == "__main__":
    TestThread().run()
