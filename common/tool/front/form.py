from .util import FontBase, to_web_view


class Form(FontBase):
    def set_row(self):
        self.form_type = "form_row"

        return self

    def set_column(self):
        self.form_type = "form_column"
        return self

    def __init__(self):
        self.body = []
        self.btns = dict(submit="提交")

    def set_btns(self, **kw):
        self.btns.update(kw)
        return self

    def set_body(self, *body: list):
        self.body = [to_web_view(d) for d in body]
        return self

    def to_json(self):
        ret = dict(type=self.form_type, childs=self.body, data=dict(btns=self.btns))
        return ret
