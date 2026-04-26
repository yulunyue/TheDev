from common.tool.export import FrontTable, Form, ConfigBase, FileConfig

from common.util.export import Node, C, ApiBase, Type


class FormBase(ApiBase):
    model: Type[FileConfig]

    def get_model(self, key):
        return getattr(self, key)

    def get(self, key, **kw):
        return self.__class__.model.get(key)

    def to_form_row_view(self):
        return Form().set_row().set_body(*self.__class__.model.get_form_columns())

    def to_form_column_view(self):
        return Form().set_column().set_body(*self.__class__.model.get_form_columns())

    def web_submit(self, type, value: dict):
        _id = self.__class__.model.get_id_any(**value)
        value = self.hander(_id, type, value)
        if value is None:
            return Node()
        if type == C.METHOD_INSERT:
            s = self.model.insert(_id, **value)
        elif type == C.METHOD_DELETE:
            s = self.model.query(_id).delete()
        elif type == C.METHOD_EDIT:
            s = self.model.query(_id).update(**value)
        else:
            raise Exception(type, value)

        s.save()
        return Node()

    def hander(self, key, type, value):
        return value

    def web_search(self, key=None, name=None, **kw):
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
