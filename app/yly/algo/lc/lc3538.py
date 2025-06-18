from common.util.export import List, functools, logger, C


class Solution:
    def get_cases(self):
        return [
            dict(l=10, n=4, k=1, position=[0, 3, 8, 10], time=[5, 8, 3, 6], result=62),
            dict(
                l=5, n=5, k=1, position=[0, 1, 2, 3, 5], time=[8, 3, 9, 3, 3], result=34
            ),
        ]

    def minTravelTime(
        self, l: int, n: int, k: int, position: List[int], time: List[int]
    ) -> int:
        rest = [0] * n
        for j in range(n - 1, 0, -1):
            rest[j - 1] = rest[j] + (position[j] - position[j - 1]) * time[j - 1]
        logger.map(rest=rest)

        @functools.lru_cache(None)
        def dfs(i, k, v):

            if i + k + 1 >= n:
                return C.inf
            if i + 1 >= n:
                return 0 if k == 0 else C.inf
            if k == 0:
                return rest[i] + v * (position[i + 1] - position[i])
            a = (position[i + 1] - position[i]) * (time[i] + v) + dfs(i + 1, k, 0)
            s = 0
            for j in range(1, k + 1):
                s += time[i + j]
                b = (position[i + 1 + j] - position[i]) * (time[i] + v) + dfs(
                    i + 1 + j, k - j, s
                )
                a = min(a, b)
            logger.map(i=i, k=k, v=v, a=a)
            return a

        return dfs(0, k, 0)
