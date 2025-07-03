from common.util.export import TestBase, logger, List, Dict
from app.xx.study import test
import _thread


class XxStudyTest(TestBase):
    def test_loop(self):
        def util(a):
            a = a + 1
            a = a - 1

        test(util)

    def test_loop1(self):
        def util(a):
            a = a + 1

        def util1(a):
            a = a - 1

        test(util)
        test(util1)

    def test_isinstace(self):
        b = []
        self.expect(isinstance(b, List[int]), True)


if __name__ == "__main__":
    XxStudyTest().run()
