from common.util.export import Dict, List, heapq, bisect, MockCf, logger


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(n=2, meetings=[[0, 10], [1, 5], [2, 7], [3, 4]], result=0),
            case1=dict(n=100, meetings=[[0, 1]], result=0),
            case2=dict(
                n=3, meetings=[[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]], result=1
            ),
        )

    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        meetings.sort()
        h = [[0, i, 0] for i in range(n)]
        for b, e in meetings:
            i = bisect.bisect_left(h, [b])
            if i > 0:
                i -= 1
            x, y, z = h.pop(i)
            nt = [max(x, b) + e - b, y, z + 1]
            h.insert(bisect.bisect_left(h, nt), nt)
            logger.info(f"b={b},e={e},h={h}")
        return sorted(h, key=lambda a: a[2])[-1][1]

    execute = mostBooked


if __name__ == "__main__":
    Solution().run()
