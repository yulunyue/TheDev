from common.algo.manage import SolutionBase,logger,MOD,bisect
from typing import List

class Solution(SolutionBase):
    uyri='https://leetcode.cn/problems/equal-sum-grid-partition-ii/'
    def get_cases(self):
        return [

        ]



    
    def execute(self, *args, **kw):
        self.init(*args, **kw)
        return self.canPartitionGrid(*args, **kw)


if __name__ == "__main__":
    Solution().run()
