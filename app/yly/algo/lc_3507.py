from common.util.export import List, MockCf, heapq, defaultdict
from common.algo.base.pn_node import PnNode


class Solution(MockCf):
    def get_cases(self):
        return dict(
            # case0=dict(nums=[5, 2, 3, 1], result=2),
            case1=dict(nums=[2, 2, -1, 3, -2, 2, 1, 1, 1, 0, -1], result=9)
        )

    def minimumPairRemoval(self, nums: List[int]) -> int:
        n = len(nums)
        nodes = PnNode.make(range(n))
        h = []
        a = d = 0
        for i in range(1, n):
            h.append((nums[i] + nums[i - 1], i - 1))
            d += 1 if nums[i - 1] > nums[i] else 0
        rf = defaultdict(int)
        heapq.heapify(h)

        # def change(n: PnNode, v):
        #     ret = 0
        #     nums[n.value] += v
        #     heapq.heappush(h, (nums[n.value], n.value))
        #     return ret

        while h and d:
            self.logger.map(d=d, h=h[0], nums=nums, ct=rf[h[0][1]])
            while h and rf[h[0][1]]:
                rf[h.pop(0)] -= 1
            if not h:
                break
            s, idx = h.pop(0)
            node: PnNode = nodes[idx]
            if node.left:
                v = nums[node.left.value]
                rf[(v + nums[idx], idx)] += 1
                heapq.heappush(h, (v + s, node.left.value))
            if node.right and node.right.right:
                v = nums[node.right.right.value]
                rf[(v + nums[idx], idx)] += 1
                heapq.heappush(h, (v + s, node.value))
            nums[idx] = s
            # d += change(node.left, nums[node.value])
            node.remove()
            # rf[node.value] = 1
            # nums[node.value] = None
            a += 1
        return a

    execute = minimumPairRemoval
