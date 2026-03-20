from common.util.export import (
    TestBase,
    logger,
    ThreadRecord,
    asset_exception,
    assert_dict,
)
from common.tool.export import (
    OsUtil,
    FileConfig,
    StrModel,
    NumberModel,
    ConfigBase,
)


class Fg(FileConfig):
    a = StrModel()
    b = NumberModel(1)


Fg.set_resource("data/test_table.json")


class TestConfig:
    def test_config(self):
        f = Fg()
        assert_dict(
            f.to_form_row_view(),
            {
                "type": "form_row",
                "childs": [
                    {"type": "input", "key": "a", "value": ""},
                    {"type": "number", "key": "b", "value": 1},
                ],
            },
        )
        m: Fg = Fg.insert("dt0")
        assert m.b.get_value(), 1
        asset_exception(
            m.b.set_value, "a", msg="[could not convert string to float: 'a'][a]"
        )
        m.update(b=2)
        assert m.b.get_value(), 2
        m.b.set_value(3)
        assert m.b.get_value(), 3
        Fg.insert("dt1")
        assert sorted([v.b.get_value() for v in Fg.all()]), [1, 3]
        assert_dict(
            Fg.to_table_view(),
            {
                "type": "table",
                "data": {
                    "header": [
                        {"type": "input", "key": "a", "value": ""},
                        {"type": "number", "key": "b", "value": 1},
                    ],
                    "body": [
                        {"_id": "dt0", "a": "", "b": 3},
                        {"_id": "dt1", "a": "", "b": 1},
                    ],
                },
            },
        )
