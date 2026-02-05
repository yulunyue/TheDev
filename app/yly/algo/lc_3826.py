from common.util.export import List, MockCf, functools, CT, bisect, heapq
from common.algo.base.pn_node import PnNode


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[1, 1, 1], k=3, result=3),
            case1=dict(nums=[1, 1, 1], k=2, result=4),
            case2=dict(nums=[13, 8, 19], k=2, result=421),
            case3=dict(nums=[5, 1, 2, 1], k=2, result=25),
            case4=dict(nums=[36, 39, 33], k=2, result=3294),
            case5=dict(nums=[3, 11, 24, 35, 8, 2], k=5, result=1057),
        )

    def minPartitionScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        nodes = PnNode.make(nums)
        heapq.heapify(nodes)
        # self.logger.map(nums=nums, k=k)
        while k < n:
            while nodes and nodes[0].is_remove:
                heapq.heappop(nodes)
            a = heapq.heappop(nodes)
            if a.right is None or (a.left and a.left.value < a.right.value):
                nd = PnNode(a.left.idx, a.left.value + a.value)
                a.left.replace(nd)
            else:
                nd = PnNode(a.right.idx, a.right.value + a.value)
                a.right.replace(nd)
            heapq.heappush(nodes, nd)
            a.remove()
            # self.logger.map(h=a.get_head().show())
            k += 1
        return (
            sum(v.value * v.value for v in nodes if not v.is_remove) + sum(nums)
        ) // 2

    execute = minPartitionScore
