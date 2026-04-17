from common.util.export import Node, List, Dict, Any
from .util import FontBase, to_web_view


class FrontTable(FontBase):
    def init(self):
        self.header: List[Dict] = []
        self.body: List[Dict] = []

    def set_header(self, *header):
        self.header = []
        for h in header:
            self.header.append(to_web_view(h))
        return self

    def set_body(self, body: list):
        self.body = body
        return self

    def append_row(self, **kw):
        self.body.append(kw)
        return self

    def get_header(self):
        return self.header

    def get_body(self):
        return self.body

    def to_json(self):
        return dict(
            type="table",
            childs=self.get_header(),
            value=self.get_body(),
        )
