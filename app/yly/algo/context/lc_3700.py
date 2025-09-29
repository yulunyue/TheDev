from common.util.export import functools, CT, logger


class Solution:
    def get_cases(self):
        return [dict(n=4, l=3, r=5, result=16)]

    def zigZagArrays(self, n: int, l: int, r: int) -> int:
        r = r - l + 1
        up = [i for i in range(r)]
        # down = [r - i - 1 for i in range(r)]
        us = sum(up)
        for _ in range(2, n):
            up1 = []
            # down1 = []
            us = 0
            for v in range(r):
                up1.append(us)
                # us -= up[v]
                # down1.append(us)
                us = (us + up[r - v - 1]) % CT.MOD
            up = up1
            # logger.map(up=up, us=us)
        return (2 * sum(up)) % CT.MOD

    execute = zigZagArrays
