from common.util.export import List, MockCf, heapq
from common.algo.base.pn_node import PnNode


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[5, 2, 3, 1], result=2),
        )

    def minimumPairRemoval(self, nums: List[int]) -> int:

        n = len(nums)
        nodes = PnNode.make(range(n - 1))
        h = [
            [
                nums[v.value] + nums[v.value + 1],
                nums[v.value],
                nums[v.value + 1],
                v,
            ]
            for v in nodes
        ]
        a = 0
        need_update = [0] * (n - 1)
        heapq.heapify(h)
        while h:
            while h and need_update[h[0][-1].value]:
                v = need_update[h[0][-1].value]
                s, l, r, n = heapq.heappop(h)
                heapq.heappush(h, [s + v, l + v, r + v, n])
                need_update[h[0][-1].value] = 0
            s, l, r, n = h.pop(0)
            node: PnNode = n

            if node.left:
                need_update[node.left.value] += r
                a += 1
            if node.right:
                need_update[node.right.value] += l
            node.remove()
            # self.logger.map(
            #     s=s,
            #     idx=node.value,
            #     need_update=need_update,
            #     h=[[v[0], v[-1].value] for v in h],
            # )
        return a

    execute = minimumPairRemoval
