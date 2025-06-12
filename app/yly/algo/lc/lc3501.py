from typing import List
from common.util.export import logger
from common.algo.base.sparsetable import SparseTable


class Solution:
    def get_cases(self):
        return [dict(s="1000100", queries=[[1, 5], [0, 6], [0, 4]], result=[6, 7, 2])]

    def maxActiveSectionsAfterTrade(self, s: str, queries: List[List[int]]):
        n = len(s)
        a = [[-1, -1]]
        b = []
        c = []
        last0_sum = 0
        total = 0
        start = 0
        for i, v in enumerate(s):
            b.append(len(a))
            if i == n - 1 or v != s[i + 1]:
                if v == "0":
                    a.append([start, i + 1])
                    c.append(last0_sum + i - 1 - start)
                    last0_sum = i + 1 - start
                start = i + 1
            total += v == "1"
        a.append([n, n])
        c.append(last0_sum)
        st = SparseTable(c)
        ans = []
        for l, r in queries:
            i, j = b[l], b[r]
            tmp = 0
            if l + 1 < len(s) and s[l] == "0" and s[l + 1] == "0":
                tmp = max(tmp, a[i][1] - l + a[i + 1][1] - a[i + 1][0])
                i += 1
            if r + 1 < len(s) and s[r] == "0" and s[r + 1] == "0":
                tmp = max(tmp, r - a[j][0] + a[j - 1][1] - a[j - 1][0])
            tmp = max(tmp, st.query_cache_max(i, j))
            logger.pt(f"l:{l}, r:{r}, s:{s[l : r + 1]}, ai:{a[i:j+1]}, sum:{tmp}")
            ans.append(tmp + total)
        return ans
