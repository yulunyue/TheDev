from common.util.export import List, MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(robots=[10, 2], distance=[5, 1], walls=[5, 2, 7], result=3)
        )

    def maxWalls(self, robots: List[int], distance: List[int], walls: List[int]) -> int:
        fl, fr, d, n = 0, 0, distance, len(robots)
        rs = robots
        m = len(d)
        rbs = sorted([[v, d[i]] for i, v in enumerate(robots)])
        walls.sort()
        lxr = lxl = float("-inf")
        wi = 0
        for i, (x, z) in enumerate(rbs):
            l = z if i == 0 else min(z, z - rbs[i - 1][0])
            r = z if i == n - 1 else min(z, rbs[i + 1][0] - z)
            xr, xl = x + r, x - l
            lcl = rcl = lcr = rcr = 0
            while wi < m and walls[wi] <= xr:
                u = walls[wi]
                if xl <= u <= x:
                    lcl += 1
                if lxl < u <= x:
                    lcr += 1
                if x <= u <= xr:
                    rcl += 1
                if lxr < u <= x:
                    rcr += 1
                wi += 1
            lxl, lxr = xl, xr
            fl = max(fl + lcl, fr + lcr)
            fr = max(fl + rcl, fr + rcr)
        return max(fl, fr)

    execute = maxWalls
