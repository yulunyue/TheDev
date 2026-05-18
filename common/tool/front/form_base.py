from common.tool.export import FrontTable, Form, ConfigBase, FileConfig

from common.util.export import Node, C, ApiBase, Type


class FormBase(ApiBase):
    model: Type[FileConfig]

    def get(self, key, **kw):
        return Node(value=self.__class__.model.get(key))

    def get_font(self, key, **kw):
        return Node(value=self.__class__.model.get(key))

    def to_form_row_view(self):
        return Form().set_body(*self.__class__.model.get_form_columns())

    def to_form_column_view(self):
        return Form().set_body(*self.__class__.model.get_form_columns())

    def web_insert(self, **value):
        _id = self.model.get_id_any(**value)
        value = self._handler_insert(_id, value)
        if value is None:
            return Node(value=False)
        self.model.insert(_id, **value).save()
        return Node(value=True)

    def web_delete(self, **value):
        _id = self.model.get_id_any(**value)
        value = self._handler_delete(_id, value)
        if value is None:
            return Node(value=False)
        self.model.query(_id).delete().save()
        return Node(value=True)

    def web_edit(self, **value):
        _id = self.model.get_id_any(**value)
        value = self._handler_edit(_id, value)
        if value is None:
            return Node(value=False)
        self.model.query(_id).update(**value).save()
        return Node(value=True)

    def _handler_insert(self, _id, value):
        return value

    def _handler_edit(self, _id, value):
        return value

    def _handler_delete(self, _id, value):
        return value

    def to_table_view(self):
        cls = self.model
        return FrontTable().set_header(*cls.get_params().values()).set_body(cls.all())
