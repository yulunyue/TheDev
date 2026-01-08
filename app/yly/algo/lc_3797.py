from common.util.export import List, MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(case0=dict(grid=["..", "#."], d=1, result=2))

    def numberOfRoutes(self, grid: List[str], d: int) -> int:
        pass


if __name__ == "__main__":
    Solution().run()
