from common.algo.manage import SolutionBase


class Solution(SolutionBase):
    def get_cases(self):
        return []

    def xx(self, *args, **kw):
        self.init(*args, **kw)
        return self.execute(*args, **kw)


if __name__ == "__main__":
    Solution().run()
