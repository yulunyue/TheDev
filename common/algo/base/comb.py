from common.util.export import CT


class Comb:
    def load(self, mx=CT.MX, mod=None):
        """(a//fac[i])%MOD == (a*self.inv_fac[i])%MOD"""
        self.mod = mod
        self.mx = mx
        # 组合数模板
        self.fac = [0] * mx
        self.fac[0] = 1
        for i in range(1, mx):
            self.fac[i] = self.calc_mod(self.fac[i - 1] * i)

        self.inv_fac = [0] * mx
        self.inv_fac[mx - 1] = self.pow(self.fac[mx - 1], -1)
        for i in range(mx - 1, 0, -1):
            self.inv_fac[i - 1] = self.calc_mod(self.inv_fac[i] * i)
        return self

    def pow(self, a, b):
        if self.mod is not None:
            return pow(a, b, self.mod)
        return pow(a, b)

    def calc_mod(self, v):
        if self.mod is None:
            return v
        return v % self.mod

    def comb(self, n: int, k: int) -> int:
        if n < k:
            raise Exception(n, k)
        if k == 0 or k == n:
            return 1
        return round(
            self.calc_mod(
                self.calc_mod(self.fac[n] * self.inv_fac[k]) * self.inv_fac[n - k]
            )
        )
