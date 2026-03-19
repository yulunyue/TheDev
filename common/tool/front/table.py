from common.util.export import Node, List, Dict, Any
from common.tool.export import FileConfig, ConfigBase


class FrontTable(Node):
    def init(self):
        self.header: List[Dict] = []
        self.body: List[Dict] = []

    def set_header(self, *header):
        self.header = []
        for h in header:
            if isinstance(h, dict):
                self.header.append(h)
            else:
                self.header.append(dict(key=h, value=h))

        return self

    def set_body(self, body):
        self.body = body
        return self

    def append_row(self, **kw):
        self.body.append(kw)
        return self

    def load_from_table(self, t: ConfigBase, **kw):
        return self.set_header(*t._concrete_type.to_web_view()).set_body(
            [v.to_json() for v in t.filter(**kw)],
        )

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
