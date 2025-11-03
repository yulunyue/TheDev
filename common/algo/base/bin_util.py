from typing import List
from common.util.export import logger

POS_MASK = [(2**i) - 1 for i in range(128)]


def encode_data(array, pos) -> int:
    """a[0] a[1] a[2]"""
    ans = array[0]
    for i in range(len(array) - 1):
        p = pos[i] if isinstance(pos, list) else pos
        ans = (ans << p) + (array[i + 1] & POS_MASK[p])
    return ans


def decode_data(mask, pos: List[int]) -> List[int]:
    ans = []
    r = 0
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


def get_sub_bits(i):
    j = i
    ret = []
    while j:
        ret.append(j)
        j = (j - 1) & i
    return ret
