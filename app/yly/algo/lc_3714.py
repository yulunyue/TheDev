from common.util.export import MockCf, defaultdict, inf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(s="abbac", result=4),
            case1=dict(s="aba", result=2),
        )

    def longestBalanced(self, s: str) -> int:
        n = len(s)
        ct = dict(a=0, b=0, c=0)
        mp = dict()
        ans = 1
        for i, v in enumerate(s):
            ct[v] += 1

            min_ct, max_ct = inf, -inf
            for u in ct.values():
                if u == 0:
                    continue
                min_ct, max_ct = min(min_ct, u), max(max_ct, u)
            if min_ct == max_ct:
                ans = i + 1
                continue
            key = ""
            for k, v in ct.items():
                if v > min_ct:
                    key += f"{k}:{v-min_ct};"

            if key in mp:
                ans = max(ans, i - mp[key] + 1)
            else:
                mp[key] = i
            self.logger.map(i=i, key=key, mp=mp)

        return ans

    execute = longestBalanced
