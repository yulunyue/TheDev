from common.util.export import TestBase
from common.third_util.export import LeetCode, EChart, Faker, opts


class ThirdTest(TestBase):
    def run_lc(self):
        l = LeetCode()
        self.expect(l.submit(), 1)


if __name__ == "__main__":
    ThirdTest().run()
