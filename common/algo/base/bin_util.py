from typing import List
from common.util.export import logger, defaultdict


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


def set_mask(mask, low_idx, num, value):
    mask_high = (mask >> (low_idx + num)) << (low_idx + num)
    mask_mid = value << low_idx
    mask_low = mask & POS_MASK[low_idx]
    ret = mask_high | mask_mid | mask_low
    # logger.info(f"{bin(mask)}\n{num}:{value}\n{bin(ret)}")
    return ret


def low_bits(j):
    ret = []
    i = j
    while i:
        low_bit = i & -i
        ret.append(low_bit)
        i -= low_bit
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


def ss_or_dp(nums):
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


def ss_or_dp(nums):
    or_all = 0
    for v in nums:
        or_all |= v
    w = or_all.bit_length()
    u = 1 << w

    f = [0] * u
    for x in nums:
        f[x] += 1
    for i in range(w):
        bit = 1 << i  # 避免在循环中反复计算 1 << i
        if (
            or_all & bit == 0
        ):  # 优化：or_all 中是 0 但 s 中是 1 的 f[s] 后面容斥用不到，无需计算
            continue
        s = 0
        while s < u:
            s |= bit  # 快速跳到第 i 位是 1 的 s
            f[s] += f[s ^ bit]
            s += 1
    return f
