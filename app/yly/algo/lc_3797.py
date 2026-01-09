from common.util.export import List, MockCf, functools, CT, math


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(
                grid=[
                    "..",
                    "#.",
                ],
                d=1,
                result=2,
            ),
            case1=dict(
                grid=["..."],
                d=1,
                result=7,
            ),
            case2=dict(
                grid=[".", ".", "."],
                d=2,
                result=1,
            ),
            case4=dict(
                grid=[
                    "..",
                    "#.",
                ],
                d=2,
                result=4,
            ),
        )

    def numberOfRoutes(self, grid: List[str], d: int) -> int:
        n, m = len(grid), len(grid[0])
        f = [0] * (m + 1)
        g = [0] * (m + 1)
        for i in range():
            pass

        return

    execute = numberOfRoutes


if __name__ == "__main__":
    Solution().run()
