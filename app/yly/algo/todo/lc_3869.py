from common.util.export import List, Dict, MockCf, functools
from common.algo.base.bin_util import low_high_dp


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(l=12340, r=12341, result=1),
            case1=dict(l=8, r=10, result=3),
        )

    def countFancy(self, l: int, r: int) -> int:
        def call_good(value, up_down, last_value, s, depth=0):
            if last_value is None:
                return up_down, value, s + value
            if up_down is None:
                if value == last_value:
                    return
                return -1 if value < last_value else 1, value, s + value
            c = value - last_value
            if c * up_down <= 0:
                return
            return up_down, value, s + value

        @functools.lru_cache(None)
        def is_up_down(v):
            v = [int(u) for u in str(v)]
            if len(v) == 2 and v[0] == v[1]:
                return 0
            for i in range(1, len(v) - 1):
                if (v[i - 1] - v[i]) * (v[i] - v[i + 1]) <= 0:
                    return 0
            return 1

        a = low_high_dp(
            l,
            r,
            None,
            None,
            0,
            calc_args=call_good,
        )
        b = low_high_dp(
            l,
            r,
            0,
            calc_args=lambda v, last_v, **kw: [v + last_v],
            ret_fun=lambda v, **kw: is_up_down(v),
        )
        c = low_high_dp(
            l,
            r,
            None,
            None,
            0,
            calc_args=call_good,
            ret_fun=lambda a, b, v, **kw: is_up_down(v),
        )
        return a + b - c

    execute = countFancy
