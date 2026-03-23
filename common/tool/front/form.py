from .util import FontBase


class Form(FontBase):
    def set_row(self):
        self.form_type = "form_row"
        self.btn_default = dict()
        return self

    def set_column(self):
        self.form_type = "form_column"
        return self

    def __init__(self):
        self.body = []

    def set_body(self, *body: list):
        self.body = [FontBase.get_dom_type(d) for d in body]
        return self

    def to_json(self):
        return dict(type=self.form_type, childs=self.body)
