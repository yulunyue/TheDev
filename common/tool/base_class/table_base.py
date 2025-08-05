from .model import NumberModel, BaseModel, StrModel, DictModel, List, Dict
from .baseconfig import ConfigBase
from ...constant import THE_DEV_CONSTANT


class TableConfig(ConfigBase):

    def get_body(self):
        return self.get_config().get(THE_DEV_CONSTANT.KEY_BODY, [])


class TestTableConfig(TableConfig):
    def __init__(self):
        self.a = StrModel()
        self.b = NumberModel()
        super().__init__()


class TableBase:
    model: TableConfig
    filter_and = None
    filter_or = None

    def get_header(self):
        return {k: m.to_web_view() for k, m in self.model._params.items()}

    def get_body(self):
        return [b.to_json() for b in self.filter()]

    def filter(self):
        ret = []
        for s in self.body:
            ret.append(s)
        return ret

    def set_model(self, model: TableConfig):
        self.body = []
        self.model = model
        for data in self.model.get_body():
            self.add_row_data(**data)
        return self

    def to_web_view(self, **kw):
        return dict(
            type=THE_DEV_CONSTANT.WEB_VIEW_TYPE_TABLE,
            data=dict(header=self.get_header(), body=self.get_body(**kw)),
        )

    def add_row_data(self, **kw):
        model = self.model.clone().load(**kw)
        self.add_row(model)
        return self

    def insert_or_update(self):
        return self

    def save(self):
        self.model.save(dict(body=self.get_body()))
        return self

    def add_row(self, model):
        self.body.append(model)
        return self
