from ..baseconfig import ConfigBase
from ...front.table import FrontTable
from ...front.form import Form
from common.util.export import Node, C


class FrontExtern(ConfigBase):
    front_apis = [
        "to_form_row_view",
        "to_table_view",
        "to_form_column_view",
        "web_search",
        "web_submit",
    ]

    def get_font_columns(self):
        return self.get_params().values()

    def to_form_row_view(self):
        return Form().set_row().set_body(*self.get_font_columns())

    def to_form_column_view(self):
        return Form().set_column().set_body(*self.get_font_columns())

    @classmethod
    def web_submit(cls, type, value: dict, **kw):
        s = cls.insert(**value)
        if type == C.METHOD_INSERT_UPDATE:
            s.save()
        return Node(value=s)

    @classmethod
    def web_search(cls, key, name, **kw):
        return Node(
            childs=[
                dict(
                    title=v._id,
                    value=v,
                )
                for v in cls.all()
            ]
        )

    @classmethod
    def to_table_view(cls):
        return FrontTable().set_header(*cls.get_params().values()).set_body(cls.all())
