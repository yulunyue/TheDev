from common.util.export import MockCf, functools


class Solution(MockCf):
    uri = "https://leetcode.cn/problems/maximize-the-number-of-partitions-after-operations/solutions/2595072/ji-yi-hua-sou-suo-jian-ji-xie-fa-pythonj-6g5z/?envType=daily-question&envId=2025-10-17"

    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:

        n = len(s)
        ct = dict()
        for i in range(26):
            ct[chr(ord("a") + i)] = ct[i] = 1 << i

        @functools.lru_cache(None)
        def dfs(i, m: int, changed):
            if i == n:
                return 1
            new_mask: int = m | ct[s[i]]
            if new_mask.bit_count() > k:
                ret = dfs(i + 1, ct[s[i]], changed) + 1
            else:
                ret = dfs(i + 1, new_mask, changed)
            if not changed:
                for j in range(26):
                    new_mask = m | ct[j]
                    if new_mask.bit_count() > k:
                        ret = max(ret, dfs(i + 1, ct[j], True) + 1)
                    else:
                        ret = max(ret, dfs(i + 1, new_mask, True))
            # self.logger.map(i=i, m=bin(m), ret=ret)
            return ret

        return dfs(0, 0, False)

    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        if k == 26:
            return 1
        seg, mask, size = 1, 0, 0

        def Update(i):
            nonlocal seg, mask, size
            bit = 1 << (ord(s[i]) - ord("a"))
            if mask & bit:
                return
            size += 1
            if size > k:
                seg += 1
                mask = bit
                size = 1
            else:
                mask |= bit

        n = len(s)
        suf = [None] * n + [(0, 0)]
        for i in range(n - 1, -1, -1):
            Update(i)
            suf[i] = (seg, mask)
        ans = seg
        seg, mask, size = 1, 0, 0
        for i in range(n):
            suf_seg, suf_mask = suf[i + 1]
            res = seg + suf_seg
            union_size = (mask | suf_mask).bit_count()
            if union_size < k:
                res -= 1
            elif union_size < 26 and size == k and suf_mask.bit_count() == k:
                res += 1
            ans = max(ans, res)
            Update(i)
        return ans

    execute = maxPartitionsAfterOperations
