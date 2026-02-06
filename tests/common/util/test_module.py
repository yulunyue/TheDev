from common.util.test import TestBase
from common.util.module import Module, get_function_info


class Cls1:
    def fun(self, key="", **kw):
        pass


def fun_call(self, a, b, d=1, f=2, **kw):
    pass


class TestModule(TestBase):
    def test_get_function_info(self):
        f = get_function_info(Cls1().fun)
        self.expect(
            f.to_json(),
            {
                "key": "fun",
                "title": "fun",
                "childs": [
                    {
                        "title": "key",
                        "default_value": "",
                        "type": "str",
                        "is_pos": False,
                        "key": "key",
                    }
                ],
            },
        )

    def test_fun_call(self):
        fun_info = get_function_info(fun_call)
        self.expect(fun_info.name, "fun_call")
        self.expect(fun_info.has_args, False)
        self.expect(fun_info.has_kw, True)
        self.expect(fun_info.args, ["a", "b"])
