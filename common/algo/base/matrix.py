from common.util.export import List, CT


class Matrix:
    def __init__(self, a):
        self.a: List[List[int]] = a
        self.n = len(a)
        self.m = len(a[0])

    def mult(self, op: "Matrix", mod=CT.MOD):
        """矩阵乘法"""

        result = [[0] * op.m for _ in range(self.n)]
        for i in range(self.n):
            for j in range(op.m):
                for k in range(op.n):
                    result[i][j] += self.a[i][k] * op.a[k][j]
                result[i][j] %= mod
        return Matrix(result)

    def copy(self):
        return Matrix([row[:] for row in self.a])

    def pow(self, base, power):
        """矩阵快速幂"""

        # 初始化结果为单位矩阵
        base = Matrix(base)
        result = self.copy()  # 深拷贝
        while power > 0:
            if power & 1:  # 如果当前位是1
                result = result.mult(base)
            base = base.mult(base)
            power >>= 1  # 右移一位
        return result
