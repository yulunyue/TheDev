from common.util.export import logger, functools

"""
    1
        1
    2
        2
    3
        12,3
    4
        4
    5
        23,14,5
    6
        24,6
    7
        7,124,34
    8
        26,8
    9
        18,126,234,27,36,45
    14
        86
    15
        78,96
"""


@functools.lru_cache(None)
def dfs(n, state):
    ret = []
    if n < 10:
        ret.append(set(n))
    for i in range(1, n):
        m = 1 << (i - 1)
        if state & m:
            continue
        dfs(n - i, state | m)
    logger.map(n=n, state=bin(state))


class Solution:
    def get_cases(self):
        return [dict(n=2, result=22)]

    def specialPalindrome(self, n: int) -> int:
        dfs(8, 0)

    def execute(self, *args, **kw):
        return self.specialPalindrome(*args, **kw)
