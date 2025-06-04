from common.util.test import TestBase, logger
from .study import test


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


if __name__ == "__main__":
    XxStudyTest().run()
