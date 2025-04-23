from common.util.export import get_function_info, TestBase


class TestCls:
    def test_fun(self, a: int, b=2):
        pass


class TestUtil(TestBase):
    def test_fun(self):
        c = TestCls()
        info = get_function_info(c.test_fun)
        self.expect(info.data["kwargs"], dict(a=None, b=2), "")


if __name__ == "__main__":
    TestUtil().run()
