from common.util.export import MockCf, defaultdict, inf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(s="abbac", result=4),
            case1=dict(s="aba", result=2),
            case2=dict(s="aabcc", result=3),
            case3=dict(s="accc", result=3),
        )

    def get_key(self, suf, ct: dict):
        min_ch, mask = "c", dict(a="", b="", c="")
        ret = []
        for j in range(len(suf) - 1, -1, -1):
            min_ch = min(min_ch, suf[j])
            d = ct.copy()
            for ch in suf[j:]:
                d[ch] -= ct[min_ch]
            mask[suf[j]] = "*"
            p = ""
            for k in "abc":
                p += f"{k}{mask[k]}{d[k]}"
            ret.append(p)
        return ret

    def longestBalanced(self, s: str) -> int:
        n = len(s)
        ct = dict(a=0, b=0, c=0)
        pos = dict()
        ans = 1
        t = ""
        sufs = [""] * n
        for i in range(n - 1, -1, -1):
            v = s[i]
            t = t.replace(v, "") + v
            sufs[i] = t
        t = ""
        # self.logger.info(s)
        for i, v in enumerate(s):
            for k in self.get_key(sufs[i], ct):
                if k not in pos:
                    pos[k] = i - 1
                    self.logger.map(i=i - 1, t1=sufs[i], k=k)
            ct[v] += 1
            t = t.replace(v, "") + v
            for k in self.get_key(t, ct):
                if k in pos:
                    ans = max(ans, i - pos[k])
                    # self.logger.map(i=i, t2=t, k=k)
        return ans

    execute = longestBalanced
