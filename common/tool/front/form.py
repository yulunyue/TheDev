from .util import FontBase, to_web_view


class Form(FontBase):

    def __init__(self):
        self.btns = dict()
        super().__init__()

    def set_btns(self, kw):
        self.btns.update(kw)
        return self

    def set_body(self, *body: list):
        self.childs = [to_web_view(d) for d in body]
        return self

    def to_json(self):
        ret = dict(type="from", childs=self.childs, data=dict(btns=self.btns))
        return ret
