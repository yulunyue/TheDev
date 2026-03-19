from common.util.export import Node, List, Dict, Any
from .util import get_dom_type


class FrontTable(Node):
    def init(self):
        self.header: List[Dict] = []
        self.body: List[Dict] = []

    def set_header(self, *header):
        self.header = []
        for h in header:
            self.header.append(get_dom_type(h))
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
            data=dict(
                header=self.get_header(),
                body=self.get_body(),
            ),
        )
