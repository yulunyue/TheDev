from common.util.export import TestBase
import numpy as np

A = [1, 2, 3, 4]
B = [[1], [2], [3], [4]]


class TestNp(TestBase):
    def test_array(self):
        a = np.array(A)
        self.expect(a.reshape((-1, 1)), B)
        c = np.eye(3, 3)
        self.expect(c, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def test_linalg(self):
        a = np.array([[1, 2], [3, 4]])
        b = np.linalg.inv(a)
        self.expect(b, [[-2, 1], [1.5, -0.5]])
        """
        1,2  * -2 , 1    = 1*-2+2*1.5=1, 1*1-2*0.5=0
        3,4    1.5,-0.5    3*-2+4*1.5=0, 3*1-4*0.5=1
        """
        self.expect(np.dot(a, b), np.eye(2))

    def test_all(self):
        self.test_array()

    def expect(self, a, e):
        if not isinstance(a, np.ndarray):
            a = np.array(a)
        if not isinstance(e, np.ndarray):
            e = np.array(e)
        if a.shape != e.shape:
            not_equ = True
        else:
            not_equ = abs((a - e).min()) > 0.00000001
        return super().expect(
            not_equ, False, info=f"{a.shape},{a}!={e.shape},{e}", stacklevel=3
        )


if __name__ == "__main__":
    TestNp().run()
