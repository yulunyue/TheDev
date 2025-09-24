from common.util.export import CT


class Comb:
    def load(self, mx=CT.MX, mod=CT.MOD):
        """(a//fac[i])%MOD == (a*self.inv_fac[i])%MOD"""
        self.mod = mod
        self.mx = mx
        # 组合数模板
        self.fac = [0] * mx
        self.fac[0] = 1
        for i in range(1, mx):
            self.fac[i] = (self.fac[i - 1] * i) % mod

        self.inv_fac = [0] * mx
        self.inv_fac[mx - 1] = pow(self.fac[mx - 1], -1, mod)
        for i in range(mx - 1, 0, -1):
            self.inv_fac[i - 1] = (self.inv_fac[i] * i) % mod
        return self

    def comb(self, n: int, k: int) -> int:
        return (
            ((self.fac[n] * self.inv_fac[k]) % self.mod)
            * self.inv_fac[n - k]
            % self.mod
        )

    def make_split(self, array, num):
        ans = []

        def dfs(i, a, b):
            if i == len(array):
                if len(a) == num:
                    ans.append([a[:], b[:]])
                return
            dfs(i + 1, a + [array[i]], b)
            dfs(i + 1, a, b + [array[i]])

        dfs(0, [], [])
        return ans
