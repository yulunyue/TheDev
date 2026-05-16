from common.util.export import (
    TestBase,
    Module,
    get_function_info,
    enum_cls,
    TypeVar,
    Generic,
)


class Cls1:
    def fun(self, key="", **kw):
        pass


def fun_call(self, a, b, d=1, f=2, **kw):
    return 1


class TestModule(TestBase):
    def test_module(self):
        Module().load_module_object("common.util.tool::uid")
        f = Module().load_module_object("app.tool.task::test")
        assert f() == dict(value=1)

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

    def test_fun_auto(self):

        def fun_call2(a: enum_cls("22")):
            pass

        fun_info = get_function_info(fun_call2).to_json()
        self.expect(
            fun_info,
            {
                "key": "fun_call2",
                "title": "fun_call2",
                "childs": [
                    {
                        "title": "a",
                        "default_value": None,
                        "type": "enum",
                        "is_pos": True,
                        "childs": ["22"],
                        "key": "a",
                    }
                ],
            },
        )
