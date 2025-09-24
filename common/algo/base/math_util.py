import math
import itertools
from functools import lru_cache
from collections import defaultdict, deque, Counter
from common.util.export import CT


@lru_cache(None)
def gcd(v1, v2):
    return gcd(v2, v1 % v2) if v2 > 0 else v1


def pi_float(v):
    if isinstance(v, int):
        return v / 180 * math.pi
    return v


def mul_rect(a, b, mod):
    ans = [[0] * len(b[0]) for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(a[i])):
                ans[i][j] = (ans[i][j] + a[i][k] * b[k][j]) % mod
    return ans


def pow_mul_rect(a, n, f0, mod):
    res = f0
    while n:
        if n & 1:
            res = mul_rect(a, res, mod)
        a = mul_rect(a, a, mod)
        n >>= 1
    return res


def calc_angle(y, x, y1, x1):
    """
    0->2*pi
    """
    a = math.atan2(y1 - y, x1 - x)
    if a < 0:
        return 2 * math.pi + a
    return a


def sin(v):
    return math.sin(pi_float(v))


def cos(v):
    return math.cos(pi_float(v))


def prime_gcds(max_value):
    ret = defaultdict(set)
    for i in range(2, max_value):
        if len(ret[i]):
            continue
        j = i
        while j < max_value:
            ret[j].add(i)
            j += i
        i += 1
    return ret


def mean(array):
    s = sum(array) / len(array)
    return sum([(v - s) ** 2 for v in array])


def decomposition_prime_factors(v):
    ret = dict()
    i = 2
    while i * i <= v:
        while v % i == 0:
            if i not in ret:
                ret[i] = 0
            ret[i] += 1
            v = v // i
        i += 1
    if v > 1:
        ret[v] = 1
    return ret


def prime_flags(max_v):
    ret = [True] * max_v
    ret[0] = False
    ret[1] = False
    for i in range(2, max_v):
        if ret[i] == False:
            continue
        ret[i] = True
        for j in range(i * i, max_v, i):
            ret[j] = False
    return ret


@lru_cache(None)
def stl_2(n, i):
    """
    第二类斯特林数
    n个人 放到i个房间, 不允许房间为空
    """
    if n < i or i == 0:
        return 0
    elif i == n or i == 1:
        return 1
    return stl_2(n - 1, i - 1) + i * stl_2(n - 1, i)


def lucas_mod(n, m, mod):
    """
    lucas定理求组合数的摸
    """
    res = 1
    while n > 0 or m > 0:
        ni = n % mod
        mi = m % mod
        if mi > ni:
            return 0
        res = res * math.comb(ni, mi) % mod
        n //= mod
        m //= mod
    return res


def china_rest_mod(n, m, p):
    """
    中国剩余定理
    """
    mod = 1
    for a in p:
        mod *= a
    ans = 0
    for a in p:
        ans += lucas_mod(n, m, a) * (mod // a)
    return ans % mod


def extended_gcd(a, b):
    if b == 0:
        return 1, 0
    s0, t0 = extended_gcd(b, a % b)
    s = t0
    t = s0 - (a // b) * t0
    return s, t


def sigmoid(x):
    import numpy as np

    return 1.0 / (1 + np.exp(-float(x)))


def atan(x):
    return math.atan(x) * 2 / math.pi


@lru_cache(None)
def jc(n):
    if n <= 2:
        return 2
    return n * jc(n - 1)
