from common.util.export import MockCf, execute_by_thread, logger

CASE0 = dict(n=3, result=6)


class Solution(MockCf):
    def init(self, n):
        self.n = n
        self.sum = 0
        self.i = 1

    def exec(self):
        while self.i <= self.n:
            self.sum += self.i
            self.i += 1

    def get_cases(self):
        return dict(case0=CASE0)


if __name__ == "__main__":
    logger.info(execute_by_thread(Solution(), CASE0))
