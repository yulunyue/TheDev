from common.tool.export import FrontTable, Form, ConfigBase

from common.util.export import Node, C, ApiBase


class FormBase(ApiBase):
    model: ConfigBase = ConfigBase

    def get(self, key, **kw):
        return self.__class__.model.get(key)

    def to_form_row_view(self):
        return Form().set_row().set_body(*self.__class__.model.get_font_columns())

    def to_form_column_view(self):
        return Form().set_column().set_body(*self.__class__.model.get_font_columns())

    def web_submit(self, type, value: dict, **kw):
        _id = value.get("_id") or value.get("title") or str(len(self.__class__.model.instance_map) + 1)
        value.pop("_id", None)
        s = self.__class__.model.insert(_id, **value)
        s.save()
        return Node(value=s)

    def web_search(self, key, name, **kw):
        return Node(
            childs=[
                dict(
                    title=v._id,
                    value=v,
                )
                for v in self.__class__.model.all()
            ]
        )

    def to_table_view(self):
        cls = self.__class__.model
        return FrontTable().set_header(*cls.get_params().values()).set_body(cls.all())
