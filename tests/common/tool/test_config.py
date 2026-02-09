from common.util.export import TestBase, logger
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
    b = NumberModel(1)


class TestConfig(TestBase):

    def test_config(self):
        t = TableBase[TableConfigTest]().set_resource("test_table")
        m = t.insert("a")
        self.expect(m.b.get_value(), 1)
        self.expect_raise_error(
            m.b.set_value, "a", error="[could not convert string to float: 'a'][a]"
        )
        m.update(b=2)
        self.expect(m.b.get_value(), 2)
        m.b.set_value(1)
        self.expect(m.b.get_value(), 1)
        self.expect(
            t.to_web_view(),
            {
                "type": "table",
                "data": {
                    "header": [
                        {"key": "a", "value": "a", "type": "str"},
                        {"key": "b", "value": "b", "type": "number"},
                        {"key": "id", "value": "id", "type": "str"},
                    ],
                    "body": [{"a": "", "b": 1, "id": "a"}],
                },
            },
        )
        t.save()
