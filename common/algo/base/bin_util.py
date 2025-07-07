from typing import List


def encode_data(array, pos):
    ans = array[-1]
    a = 0
    for i in range(len(array) - 2, -1, -1):
        a += pos[i]
        ans += array[i] << a
    return ans


def decode_data(mask, pos: List[int]) -> List[int]:
    ans = []
    while pos:
        i = pos.pop()
        m = 1 << i
        ans.insert(0, mask & (m - 1))
        mask = mask >> i
    ans.insert(0, mask)
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
