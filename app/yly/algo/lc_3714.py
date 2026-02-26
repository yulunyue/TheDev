from common.util.export import MockCf, defaultdict


class Solution(MockCf):
    def get_cases(self):
        return dict(case0=dict(s="abbac", result=4))

    def longestBalanced(self, s: str) -> int:
        n = len(s)
        ct = dict(a=0, b=0, c=0)
        keys = "abc"
        mp = dict()
        ans = 1
        for i, v in enumerate(s):
            ct[v] += 1
            min_ct = min(ct.values())
            key = ""
            for k in keys:
                key += str(ct[k] - min_ct)
            if key in mp:
                ans = max(ans, i - mp[key] + 1)
            else:
                mp[key] = i
            # self.logger.map(i=0, key=key, mp=mp)

        return ans

    execute = longestBalanced
