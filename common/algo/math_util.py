import math
import itertools
from functools import lru_cache
from collections import defaultdict, deque, Counter


def pi_float(v):
    if isinstance(v, int):
        return v/180*math.pi
    return v


def mul_rect(a, b, mod):
    ans = [[0]*len(b[0]) for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(a[i])):
                ans[i][j] = (ans[i][j]+a[i][k]*b[k][j]) % mod
    return ans


def pow_mul_rect(a, n, f0, mod):
    res = f0
    while n:
        if n & 1:
            res = mul_rect(a, res, mod)
        a = mul_rect(a, a, mod)
        n >>= 1
    return res


def setbit(x, n):
    return x | 1 << n


def clrbit(x, n):
    return x & ~(1 << n)


def calc_angle(y, x, y1, x1):
    '''
    0->2*pi
    '''
    a = math.atan2(y1-y, x1-x)
    if a < 0:
        return 2*math.pi+a
    return a


def sin(v):
    return math.sin(pi_float(v))


def cos(v):
    return math.cos(pi_float(v))


def prime_gcds(max_value):
    ret = defaultdict(lambda: set())
    for i in range(2, max_value):
        if len(ret[i]):
            continue
        j = i
        while j < max_value:
            ret[j].add(i)
            j += i
        i += 1
    return ret


def decomposition_prime_factors(v):
    ret = dict()
    i = 2
    while i*i <= v:
        while v % i == 0:
            if i not in ret:
                ret[i] = 0
            ret[i] += 1
            v = v//i
        i += 1
    if v > 1:
        ret[v] = 1
    return ret


def prime_flags(max_v):
    ret = [True]*max_v
    ret[0]=False
    ret[1]=False
    for i in range(2, max_v):
        if ret[i] == False:
            continue
        ret[i] = True
        for j in range(i*i, max_v, i):
            ret[j] = False
    return ret


@lru_cache(None)
def stl_2(n, i):
    '''
    第二类斯特林数
    n个人 放到i个房间, 不允许房间为空
    '''
    if n < i or i == 0:
        return 0
    elif i == n or i == 1:
        return 1
    return stl_2(n-1, i-1)+i*stl_2(n-1, i)


class Comb:
    def __init__(self, mod, mx):

        self.mod = mod
        self.mx = mx
        # 组合数模板
        self.fac = [0] * mx
        self.fac[0] = 1
        for i in range(1, mx):
            self.fac[i] = self.fac[i - 1] * i % mod

        self.inv_fac = [0] * mx
        self.inv_fac[mx - 1] = pow(self.fac[mx - 1], -1, mod)
        for i in range(mx - 1, 0, -1):
            self.inv_fac[i - 1] = self.inv_fac[i] * i % mod

    def comb(self, n: int, k: int) -> int:
        return self.fac[n] * self.inv_fac[k] % self.mod * self.inv_fac[n - k] % self.mod
