from common.util.export import List, MockCf, bisect


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(robots=[10, 2], distance=[5, 1], walls=[5, 2, 7], result=3),
            case1=dict(
                robots=[17, 59, 32, 11, 72, 18],
                distance=[5, 7, 6, 5, 2, 10],
                walls=[
                    17,
                    25,
                    33,
                    29,
                    54,
                    53,
                    18,
                    35,
                    39,
                    37,
                    20,
                    14,
                    34,
                    13,
                    16,
                    58,
                    22,
                    51,
                    56,
                    27,
                    10,
                    15,
                    12,
                    23,
                    45,
                    43,
                    21,
                    2,
                    42,
                    7,
                    32,
                    40,
                    8,
                    9,
                    1,
                    5,
                    55,
                    30,
                    38,
                    4,
                    3,
                    31,
                    36,
                    41,
                    57,
                    28,
                    11,
                    49,
                    26,
                    19,
                    50,
                    52,
                    6,
                    47,
                    46,
                    44,
                    24,
                    48,
                ],
                result=37,
            ),
        )

    def maxWalls(self, robots: List[int], distance: List[int], walls: List[int]) -> int:
        fl, fr, n = 0, 0, len(robots)
        rbs = sorted([[v, distance[i]] for i, v in enumerate(robots)])
        walls.sort()
        lxr = lxl = None

        def calc_ct(l, r):
            if l > r:
                return 0
            ret = bisect.bisect_right(walls, r) - bisect.bisect_left(walls, l)
            self.log(l=l, r=r, a=ret)
            return ret

        self.log(walls=walls)
        for i, (x, z) in enumerate(rbs):
            xl, xr = x - z, x + z
            if i > 0 and xl <= rbs[i - 1][0]:
                xl = rbs[i - 1][0] + 1
            if i < n - 1 and xr >= rbs[i + 1][0]:
                xr = rbs[i + 1][0] - 1
            nfl = fl + calc_ct(xl, x)
            if lxl is not None:
                nfl = max(nfl, fr + calc_ct(max(lxr + 1, xl), x))
            nfr = max(fl, fr) + calc_ct(x, xr)
            fl, fr = nfl, nfr
            self.log(i=i, x=x, z=z, xl=xl, xr=xr, fl=fl, fr=fr)
            lxl, lxr = xl, xr
        return max(fl, fr)

    execute = maxWalls
