from common.util.export import functools, C, logger


class Solution:
    def get_cases(self):
        return [dict(l="23", r="28", b=8, result=3), dict(l="2", r="7", b=2, result=2)]

    def counterNumber(self, l: int, r: int, b: int):

        def trans(s, b):
            s = int(s)
            rt = []
            while s:
                s, r = divmod(s, b)
                rt.append(r)
            return rt[::-1]

        l, r = trans(l, b), trans(r, b)
        n = len(r)
        l = [0] * (n - len(l)) + l
        # logger.map(l=l, r=r)

        @functools.lru_cache(None)
        def dfs(i, last, lowlimit, uplimit):
            if i == n:
                return 1
            lv = max(l[i] if lowlimit else 0, last)
            rv = (r[i] + 1) if uplimit else b
            ans = 0
            for v in range(lv, rv):
                li = lowlimit and v == l[i]
                ui = uplimit and v == r[i]
                ans += dfs(i + 1, v, li, ui)
            # logger.map(i=i, last=last, lv=lv, rv=rv, ans=ans)
            return ans % C.MOD

        return dfs(0, 0, True, True)
