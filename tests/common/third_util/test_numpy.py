from common.third_util.np_util import np
from common.util.export import TestBase


class TestNumpy(TestBase):
    def expect(self, a, expect_value=True, info="", stacklevel=2):
        if isinstance(a, np.ndarray) and not isinstance(expect_value, np.ndarray):
            expect_value = np.array(expect_value)
        if isinstance(a, np.ndarray):
            a = (a == expect_value).all()
            expect_value = True
        return super().expect(a, expect_value, info, stacklevel)

    def test_base(self):
        a = np.array([[1, 2, 3], [4, 3, 2]])
        self.expect(a.shape, (2, 3))
        b = a.reshape(3, -1)  # -1 表示自动计算
        self.expect(b.shape, (3, 2))
        a[0][:] = 1.0
        self.expect(a == [[1, 1, 1], [4, 3, 2]])
        self.expect(a[0] == 1)
