from common.util.export import List, logger


class GaussElimination:
    def __init__(self, a, b):
        self.a = a
        self.n = len(a)
        self.b = b

    def calc(self):
        # 消元过程
        # self.log()
        for i in range(0, self.n - 1):
            for j in range(i + 1, self.n):
                c = -self.a[j][i] / self.a[i][i]  # 计算乘数，使得 a[j][i] 消为 0
                for k in range(0, self.n):
                    self.a[j][k] += self.a[i][k] * c  # 对应系数更新
                self.b[j] += self.b[i] * c  # 更新常数项
                # self.log()

        # # 回代过程
        x = [0] * self.n
        x[-1] = self.b[-1] / self.a[-1][-1]  # 计算最后一个变量
        for i in range(self.n - 2, -1, -1):
            for j in range(i + 1, self.n):
                self.b[i] -= self.a[i][j] * x[j]  # 更新常数项，减去已知解的影响
            x[i] = self.b[i] / self.a[i][i]  # 计算当前变量
        return x

    def log(self):
        logger.debug(f"-----------")
        for i in range(self.n):
            logger.debug(f"{self.a[i]},{self.b[i]}")
        logger.debug(f"-----------")
