from typing import List

POS_MASK = [(2**i) - 1 for i in range(24)]


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


def set_mask(mask, low_idx, high_idx, value):
    mask_high = mask >> high_idx
    mask_mid = (mask_high << (high_idx - low_idx)) + value
    return (mask_mid << low_idx) + (mask & ((1 << low_idx) - 1))


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
