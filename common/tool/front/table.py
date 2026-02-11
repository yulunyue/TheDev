from common.util.node import Node
from common.tool.export import TableBase, ConfigBase


class FrontTable(Node):
    def init(self):
        self.header = dict()
        self.body = dict()

    def set_header(self, header):
        self.header = header
        return self

    def set_body(self, body):
        self.body = body
        return self

    def load_from_table(self, t: TableBase[ConfigBase], **kw):
        return self.set_header(t._concrete_type.to_web_view()).set_body(
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
