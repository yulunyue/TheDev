from .model import NumberModel, BaseModel, StrModel, DictModel, List, Dict
from .baseconfig import ConfigBase
from ...constant import THE_DEV_CONSTANT
from common.util.export import File, TypeVar, Generic, get_origin, get_args


class TableConfig(ConfigBase):
    pass


T = TypeVar("T")


class TableBase(Generic[T]):
    _concrete_type: ConfigBase = None
    filter_and = None
    filter_or = None

    def __class_getitem__(cls, item):
        # 创建新类时保存具体类型（如 int）
        new_class = super().__class_getitem__(item)
        new_class._concrete_type = item
        return new_class

    def __new__(cls):
        ret = super().__new__(cls)
        ret._concrete_type = cls._concrete_type
        return ret

    def set_resource(self, fp):
        if isinstance(fp, str):
            fp = File(f"data/setting/{fp}.json")
        self.fp = fp
        self.config = dict()
        self.instance_map = dict()
        if self.fp.exists():
            self.config.update(self.fp.read_file())
        else:
            self.fp.write_file(dict())
        return self

    def get_header(self):
        return {k: m.to_web_view() for k, m in self._concrete_type._params.items()}

    def get_body(self):
        return [b.to_json() for b in self.filter()]

    def filter(self):
        ret = []
        for s in self.body:
            ret.append(s)
        return ret

    def to_web_view(self, **kw):
        return dict(
            type=THE_DEV_CONSTANT.WEB_VIEW_TYPE_TABLE,
            data=dict(header=self.get_header(), body=self.get_body(**kw)),
        )

    def insert(self, id, **kw) -> T:
        return self.get(id).update(**kw)

    def get(self, key) -> T:
        if key in self.instance_map:
            return self.instance_map[key]
        if key in self.config:
            config = self.config[key]
        else:
            config = self._concrete_type.get_default_conifg()
        self.instance_map[key] = self._concrete_type(key).set_resource(self)
        self.instance_map[key].update(**config)
        return self.instance_map[key]

    def save(self):
        self.fp.write_file(self.config)
        return self

    def update_param_value(self, row: ConfigBase, ins: BaseModel, vlaue):
        self.config[row.key][ins.key] = vlaue

    def get_param_value(self, row: ConfigBase, ins: BaseModel):
        return self.config[row.key][ins.key]
