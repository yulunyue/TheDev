from common.util.export import List, MockCf
from common.algo.base.persistent_segment_tree import D3SegmentTree


class St(D3SegmentTree):
    sm = 0

    def do(self, v=0):
        self.sm += v
        self.cnt += v != 0

    def up(self):
        self.cnt = self.left.cnt + self.right.cnt
        self.sm = self.left.sm + self.right.sm

    def query(self, l: "D3SegmentTree", i: int):
        if self.r <= i:
            pass


class Solution(MockCf):
    def minOperations(
        self, nums: List[int], k: int, queries: List[List[int]]
    ) -> List[int]:
        ans = []
        n = len(nums)
        left = [0] * n
        for i in range(1, n):
            left[i] = left[i - 1] if nums[i] % k == nums[i - 1] % k else 0
        st = sorted(set([v // k for v in nums]))
        mp = {v: i for i, v in enumerate(st)}
        root = St().set_range(0, len(mp) - 1).build()
        ss: List[St] = [root]
        for v in nums:
            ss.append(ss[-1].add(mp[v]))
        for l, r in queries:
            if left[r] > l:
                ans.append(-1)
                continue

        return ans

    execute = minOperations
