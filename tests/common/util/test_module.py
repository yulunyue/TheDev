from common.util.export import TestBase, Module, get_function_info


class Cls1:
    def fun(self, key="", **kw):
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
