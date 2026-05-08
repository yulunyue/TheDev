from common.util.export import List, Dict, functools, CT


class Solution:
    def balancedString(self, s: str) -> int:
        ct = dict(Q=0, W=0, E=0, R=0)
        n = len(s)
        for v in s:
            ct[v] += 1
        return
