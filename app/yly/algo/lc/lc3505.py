from typing import List
import bisect
from common.algo.base.lazyheap import LazyHeapMinMax


class Solution:
    def get_cases(self):
        return [dict(nums=[3, 2, 4, 7, 1, 5, 4], k=2, x=3, result=0)]

    def minOperations(self, nums: List[int], k=int, x=int):
        """
        中位数定理 一个区间的最小代价为这个区间所有数到中位数的具体
        """
        h = LazyHeapMinMax()
        values = []
        st = []
        x -= 1
        mid = x // 2
        for i, v in enumerate(nums):
            j = bisect.bisect_left(st, v)
            st.insert(j, v)
            if i == x:
                values.append(
                    [
                        st[mid],
                        st[mid] * mid - sum(st[:mid]),
                        sum(st[mid + 1 :]) - st[mid] * (x - mid),
                    ]
                )
            elif i > x:
                last_mid_value, last_l, last_r = values[-1]
                remove_v, new_v, mid_value = nums[i - x - 1], v, st[mid]
                new_l = last_l + (mid_value - last_mid_value) * mid
                new_r = last_r + (last_mid_value - mid_value) * (x - mid + 1)
                if remove_v < mid_value and new_v < mid_value:
                    new_l += abs(remove_v - new_v)
                elif remove_v >= mid_value and new_v >= mid_value:
                    new_r += abs(remove_v - new_v)
                elif remove_v < mid_value and new_v >= mid_value:
                    new_l += abs(remove_v - last_mid_value)
                    new_r += abs(new_v - mid_value)
                else:
                    new_l += abs(new_v - mid_value)
                    new_r += abs(remove_v - last_mid_value)
                values.append([mid_value, new_l, new_r])
            print(values[-1], nums[i - x : i + 1])
            if i >= x:
                j = bisect.bisect_left(st, nums[i - x])
                st.pop(j)
