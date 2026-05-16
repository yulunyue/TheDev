from common.util.export import (
    TestBase,
    logger,
    ThreadRecord,
    assert_dict,
)
from common.tool.export import (
    OsUtil,
    FileConfig,
    StrModel,
    NumberModel,
    ConfigBase,
    FormBase,
)

import pytest


class FgBase(FileConfig):
    a = StrModel()
    b = NumberModel(1)


FgBase.set_resource("data/test_table.json")


class Fm(FormBase):
    model = FgBase


class TestConfig:

    @pytest.mark.parametrize("f_cls", [Fm])
    def test_front(self, f_cls: FormBase):
        f: FormBase = f_cls()
        assert_dict(
            f.to_form_row_view(),
            {
                "type": "from",
                "childs": [
                    {
                        "type": "input",
                        "key": "a",
                        "value": "",
                        "title": "a",
                        "data": {"layout": None},
                    },
                    {
                        "type": "number",
                        "key": "b",
                        "value": 1,
                        "title": "b",
                        "data": {"layout": None},
                    },
                ],
                "data": {"btns": {}},
            },
        )
        # assert_dict(
        #     f.to_table_view(),
        #     {
        #         "type": "table",
        #         "data": {
        #             "header": [
        #                 {"type": "input", "key": "a", "value": ""},
        #                 {"type": "number", "key": "b", "value": 1},
        #             ],
        #             "body": [
        #                 {"_id": "dt0", "a": "", "b": 3},
        #                 {"_id": "dt1", "a": "", "b": 1},
        #             ],
        #         },
        #     },
        # )

    @pytest.mark.parametrize("Fg", [FgBase])
    def test_config(self, Fg: FgBase):
        m: FgBase = Fg.insert("dt0")
        assert m.b.get_value(), 1
        assert m.b.get_value(), 1
        m.b.set_value("a")
        assert m.b.get_value() == 1
        m.update(b=2)
        assert m.b.get_value(), 2
        m.b.set_value(3)
        assert m.b.get_value(), 3
        Fg.insert("dt1")
        assert sorted([v.b.get_value() for v in Fg.all()]), [1, 3]
