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
    resource_path = "data/test_table.json"
    a = StrModel()
    b = NumberModel(1)


Fg.init_param()


class TestConfig:
    def test_config(self):
        assert_dict(
            Fg.to_form_view(),
            {
                "type": "form",
                "childs": [
                    {"type": "str", "key": "a", "defaullt_value": ""},
                    {"type": "number", "key": "b", "defaullt_value": 1},
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
                        {"type": "str", "key": "a", "defaullt_value": ""},
                        {"type": "number", "key": "b", "defaullt_value": 1},
                    ],
                    "body": [
                        {"_id": "dt0", "a": "", "b": 3},
                        {"_id": "dt1", "a": "", "b": 1},
                    ],
                },
            },
        )
