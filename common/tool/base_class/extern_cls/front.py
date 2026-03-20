from ..baseconfig import ConfigBase
from ...front.table import FrontTable
from ...front.form import Form


class FrontExtern(ConfigBase):
    front_apis = ["to_form_row_view", "to_table_view", "to_form_column_view"]

    @classmethod
    def get_font_columns(cls):
        return cls.get_params().values()

    @classmethod
    def to_form_row_view(cls):
        return Form().set_row().set_body(*cls.get_font_columns())

    @classmethod
    def to_form_row_view(cls):
        return Form().set_column().set_body(*cls.get_font_columns())

    @classmethod
    def to_table_view(cls):
        return FrontTable().set_header(*cls.get_params().values()).set_body(cls.all())
