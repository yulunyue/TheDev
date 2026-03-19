from common.util.export import TestBase, logger, ThreadRecord
from common.tool.export import (
    OsUtil,
    FileConfig,
    StrModel,
    NumberModel,
    ConfigBase,
)


class Fg(FileConfig):
    resource_path = "data/test_table.json"
    a = StrModel()
    b = NumberModel(1)


class TestConfig:

    def test_config(self):
        Fg.init_param()
        m: Fg = Fg.insert("a")
        assert m.b.get_value(), 1

        self.expect_raise_error(
            m.b.set_value, "a", error="[could not convert string to float: 'a'][a]"
        )

        m.update(b=2)
        self.expect(m.b.get_value(), 2)

        m.b.set_value(3)
        self.expect(m.b.get_value(), 3)

        m2 = t.insert("p2")
        self.expect(m2.b.get_value(), 1)

        self.expect([v.b.get_value() for v in t.all()], [3, 1])

        # self.expect(
        #     t.to_web_view(),
        #     {
        #         "type": "table",
        #         "data": {
        #             "header": [
        #                 {"key": "a", "value": "a", "type": "str"},
        #                 {"key": "b", "value": "b", "type": "number"},
        #                 {"key": "id", "value": "id", "type": "str"},
        #             ],
        #             "body": [{"a": "", "b": 1, "id": "a"}],
        #         },
        #     },
        # )
