from common.util.export import List, defaultdict, CT, math, functools


class Solution:
    def get_cases(self):
        return [dict(nums=[1, 1, 1], queries=[[0, 2, 1, 4]], result=4)]

    def xorAfterQueries(self, nums: List[int], queries: List[List[int]]) -> int:
        n = len(nums)
        B = math.isqrt(len(queries))
        groups = defaultdict(list)

        def bl(l, r, v, k):
            for i in range(l, r + 1, k):
                nums[i] = nums[i] * v % CT.MOD

        for l, r, k, v in queries:
            if k < B:
                groups[k].append((l, r, v))
            else:
                bl(l, r, v, k)
        for k, g in groups.items():
            buckets = defaultdict(list)
            for t in g:
                buckets[t[0] % k].append(t)
            for start, bucket in buckets.items():
                if len(bucket) == 1:
                    bl(*bucket[0], k)
                    continue
                m = (n - start - 1) // k + 1
                diff = [1] * (m + 1)
                for l, r, v in bucket:
                    li = l // k
                    diff[li] = diff[li] * v
                    ri = (r - start) // k + 1
                    diff[ri] = diff[ri] * pow(v, -1, CT.MOD) % CT.MOD
                mul_d = 1
                for i in range(m):
                    mul_d = mul_d * diff[i]
                    j = start + i * k
                    nums[j] = nums[j] * mul_d % CT.MOD

        return functools.reduce(lambda a, b: a ^ b, nums)

    def execute(self, *args, **kw):
        return self.xorAfterQueries(*args, **kw)
