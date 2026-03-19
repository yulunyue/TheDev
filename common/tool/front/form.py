from .util import get_dom_type


class Form:
    def __init__(self):
        self.body = []

    def set_body(self, *body: list):
        self.body = [get_dom_type(d) for d in body]
        return self

    def to_json(self):
        return dict(type="form", data=self.body)
