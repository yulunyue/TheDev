class Solution:
    def get_cases(self):
        return dict(case0=dict(s="abbac", result=4))

    def longestBalanced(self, s: str) -> int:
        n = len(s)
        ans = 1
        ct = {chr(v): 1 for v in range(ord("a"), ord("z") + 1)}
        t = [ct]
        for i, v in enumerate(s):
            c = t[-1].copy()
            c[v] += 1
            for j in range(i + 1 - ans + 1):
                le = None
                for k, u in c.items():
                    e = u - t[j][k]
                    if e == 0:
                        continue
                    elif le is None:
                        le = e
                    elif le != e:
                        le = None
                        break
                if le is not None:
                    ans = max(ans, i - j + 1)
            t.append(c)
        return ans
