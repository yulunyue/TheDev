from common.util.export import TestBase, logger
from common.tool.export import (
    ThreadRecord,
    OsUtil,
    TableBase,
    StrModel,
    NumberModel,
    TableConfig,
    ConfigBase,
    TestRc,
)


class TestTableConfig(TableConfig):
    a = StrModel()
    b = NumberModel()


class ToolTest(TestBase):

    def test_config(self):
        t = TableBase[TestTableConfig]().set_resource("data/setting/test_table.json")
        m = t.insert("a")
        self.expect(m.b.get_value(), 1)
        m.update(b=2)
        self.expect(m.b.get_value(), 2)
        m.b.set_value(1)
        self.expect(m.b.get_value(), 1)
        t.save()


if __name__ == "__main__":
    ToolTest().run()
