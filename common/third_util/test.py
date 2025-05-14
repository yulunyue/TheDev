from common.util.export import TestBase
from common.third_util.export import LeetCode
class ThirdTest(TestBase):
    def test_lc(self):
        l=LeetCode()
        self.expect(l.submit(),1)
        # self.expect(l.check(),1)

if __name__ == '__main__':
    ThirdTest().run()