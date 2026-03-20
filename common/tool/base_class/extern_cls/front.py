from ..baseconfig import ConfigBase
from ...front.table import FrontTable
from ...front.form import Form


class FrontExtern(ConfigBase):
    front_apis = ["to_form_row_view", "to_table_view", "to_form_column_view"]

    def get_font_columns(self):
        return self.get_params().values()

    def to_form_row_view(self):
        return Form().set_row().set_body(*self.get_font_columns())

    def to_form_column_view(self):
        return Form().set_column().set_body(*self.get_font_columns())

    @classmethod
    def to_table_view(cls):
        return FrontTable().set_header(*cls.get_params().values()).set_body(cls.all())
