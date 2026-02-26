from common.util.export import MockCf, defaultdict, inf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(s="abbac", result=4),
            case1=dict(s="aba", result=2),
            case2=dict(s="aabcc", result=3),
        )

    def longestBalanced(self, s: str) -> int:
        n = len(s)
        ct = dict(a=0, b=0, c=0)
        mp = dict()
        ans = 1
        for i, v in enumerate(s):
            ct[v] += 1
            min_ct, max_ct, key = inf, -inf, "c"
            nm = 0
            for k, u in ct.items():
                # if u == 0:
                #     continue
                if u < min_ct:
                    key, min_ct = k, u
                if u == min_ct:
                    key = min(k, key)
                if u > max_ct:
                    max_ct = u
                if u:
                    nm += 1
            if nm * max_ct == i + 1:
                ans = i + 1
            for k in "abc":
                # if ct[k] == 0:
                #     continue
                if ct[k] >= min_ct:
                    key += f"{ct[k]-min_ct}"

            if key in mp:
                ans = max(ans, i - mp[key])
            else:
                mp[key] = i

            # if max_ct == min_ct:
            #     ans = i + 1
            self.logger.map(i=i, key=key, mp=mp, min_ct=min_ct, max_ct=max_ct, nm=nm)

        return ans

    execute = longestBalanced
