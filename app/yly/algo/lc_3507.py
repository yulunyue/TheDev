from common.util.export import List, MockCf, heapq, defaultdict
from common.algo.base.pn_node import PnNode


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case2=dict(nums=[5, 1, 2, 3], result=2),
            # case0=dict(nums=[5, 2, 3, 1], result=2),
            # case1=dict(nums=[2, 2, -1, 3, -2, 2, 1, 1, 1, 0, -1], result=9),
        )

    def minimumPairRemoval(self, nums: List[int]) -> int:
        n = len(nums)
        Solution.d = 0

        class Pn:
            def __init__(self, v):
                self.value = [nums[i] + nums[i + 1], i]
                self.l = nums[i]
                self.r = nums[i + 1]
                Solution.d += 1 if nums[i] > nums[i + 1] else 0

        h = Pn.make(range(n - 1))
        a = 0

        while d:
            self.logger.map(d=d, h=h, a=a)
            node: PnNode = h.pop(0)
            d -= node.remove()
            a += 1
        return a

    execute = minimumPairRemoval
