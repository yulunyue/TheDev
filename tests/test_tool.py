from common.util.export import TestBase, logger, get_function_info
from common.tool.export import (
    ThreadRecord,
    OsUtil,
    TableBase,
    StrModel,
    NumberModel,
    TableConfig,
    ConfigBase,
)


class TableConfigTest(TableConfig):
    a = StrModel()
    b = NumberModel()


def fun_call(self, a, b, d=1, f=2, **kw):
    pass


class ToolTest(TestBase):

    def test_config(self):
        t = TableBase[TableConfigTest]().set_resource("data/setting/test_table.json")
        m = t.insert("a")
        self.expect(m.b.get_value(), 1)
        m.update(b=2)
        self.expect(m.b.get_value(), 2)
        m.b.set_value(1)
        self.expect(m.b.get_value(), 1)
        t.save()

    def test_fun_call(self):
        fun_info = get_function_info(fun_call)
        self.expect(fun_info.name, "fun_call")
        self.expect(fun_info.has_args, False)
        self.expect(fun_info.has_kw, True)
        self.expect(fun_info.args, ["self", "a", "b"])
        self.expect(
            fun_info.kw,
            {
                "a": {"key": "a", "default_value": None, "type": None, "is_pos": True},
                "b": {"key": "b", "default_value": None, "type": None, "is_pos": True},
                "d": {"key": "d", "default_value": 1, "type": "int", "is_pos": False},
                "f": {"key": "f", "default_value": 2, "type": "int", "is_pos": False},
            },
        )


if __name__ == "__main__":
    ToolTest().run()
