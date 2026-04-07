from common.util.export import (
    MockCf,
    execute_by_thread,
    logger,
    json_dumps,
    File,
    exec_thread_recode_file,
)
from common.tool.export import ArrayWithArrow

CASE0 = dict(nums=[4, 5, 7], result=6)


class Solution(MockCf):
    def init(self, nums):
        self.s = ArrayWithArrow().set_arrow(1).set_nums(nums)
        self.sum = 0

    def exec(self):
        while self.s.i < self.s.n:
            self.sum += self.s.nums[self.s.i]
            self.s.i += 1

    def get_cases(self):
        return dict(case0=CASE0)


if __name__ == "__main__":
    exec_thread_recode_file(Solution, "case0")
