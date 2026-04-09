from typing import List
from common.util.export import logger, defaultdict, functools


def p2(num=10**6, mod=None, extern=1):
    result = [0]
    for i in range(1, num):
        result.append(result[i - 1] * 2 + extern)
        if mod is not None:
            result[-1] = result[-1] % mod
    return result


POS_MASK = p2(256)


def encode_data(array, pos) -> int:
    """a[0] a[1] a[2]"""
    ans = 0
    for i in range(len(array)):
        p = pos[i] if isinstance(pos, list) else pos
        ans = (ans << p) + (array[i] & POS_MASK[p])
    return ans


def decode_data(mask, pos: List[int]) -> List[int]:
    ans = []
    while pos:
        p = pos.pop()
        ans.insert(0, mask & POS_MASK[p])
        mask >>= p

    return ans


def set_mask(num, start, length, value):
    mask = POS_MASK[length] << start
    num = num & ~mask
    return num | ((value << start) & mask)


def low_bits(j):
    ret = []
    i = j
    while i:
        low_bit = i & -i
        ret.append(low_bit)
        i ^= low_bit
    return ret


def get_sub_bits(i) -> List[int]:
    j = i
    ret = []
    while True:
        ret.append(j)
        if j == 0:
            break
        j = (j - 1) & i
    return ret


def get_sub_bit2(i):
    """
    子集分成小，大两份，不包括自己
    """
    mx = (i - 1) & i
    mn = i ^ mx
    ret = []
    while mn < mx:
        ret.append([mn, mx])
        mx = (mx - 1) & i
        mn = i ^ mx
    return ret


def ss_or_dp(nums):  # 返回的是 2**x
    xor_all = 0
    for v in nums:
        xor_all |= v
    f = [0] * (xor_all + 1)
    for v in nums:
        f[v] += 1
    n = xor_all.bit_length()
    for i in range(n):
        u = 1 << i
        v = 0
        while v <= xor_all:
            v = v | u
            f[v] += f[v ^ u]
            v += 1
    return f


def low_high_dp(low, high, *args, calc_args=None, ret_fun=None):
    """
    ret_fun(*args, depth) -> bool:
    calc_args(v,*args,depth)-> args
    求能被3整除
    def calc_args(v, a, depth):
        return [(v + a) % 3]

    def ret_fun(v, depth):
        return v == 0
    args = (0,)
    """
    if isinstance(low, int):
        low = [int(v) for v in str(low)]
    if isinstance(high, int):
        high = [int(v) for v in str(high)]
    low = [0] * (len(high) - len(low)) + low

    @functools.lru_cache(None)
    def dfs(i, low_limit, high_limit, *args, first_zero=True):
        if i >= len(high):
            return (
                1 if ret_fun is None else ret_fun(*args, depth=i, first_zero=first_zero)
            )
        l = low[i] if low_limit else 0
        h = high[i] if high_limit else 9
        a = 0
        for v in range(l, h + 1):
            fz = first_zero and v == 0
            argsi = args
            if calc_args:
                argsi = calc_args(v, *args, depth=i, first_zero=fz)
                if argsi is None:
                    continue
            a += dfs(
                i + 1,
                low_limit and v == l,
                high_limit and v == h,
                *argsi,
                first_zero=fz
            )
        return a

    return dfs(0, True, True, *args)


def to_2(v: int, n: int):
    ans = [0] * n
    t = 0
    while v:
        if v & 1:
            ans[n - t - 1] = 1
        v = v >> 1
        t += 1
    return ans, t
