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
            fp = File(f"config/setting/{fp}.json")
        self.fp = fp
        self.config = dict()
        self.instance_map: Dict[str, ConfigBase] = dict()
        if self.fp.exists():
            self.config.update(self.fp.read_file())
        else:
            self.fp.write_file(dict())
        return self

    def filter(self) -> List[T]:
        ret = []
        for k in self.config.keys():
            v = self.get(k)
            ret.append(v)
        return ret

    def all(self):
        return self.filter()

    def to_web_view(self, **kw):
        return dict(
            type=THE_DEV_CONSTANT.WEB_VIEW_TYPE_TABLE,
            data=dict(header=self.get_header(), body=self.get_body(**kw)),
        )

    def insert(self, id, **kw) -> T:
        r: ConfigBase = self.get(id)
        return r.update(**kw)

    def get(self, key) -> T:
        if key in self.instance_map:
            return self.instance_map[key]
        if key in self.config:
            config = self.config[key]
        else:
            self.config[key] = config = self._concrete_type.get_default_conifg()
        self.instance_map[key] = self._concrete_type(key)
        self.instance_map[key].set_resource(self).update(**config)
        return self.instance_map[key]

    def save(self):
        self.fp.write_file(self.config)
        return self

    def update_param_value(self, row: ConfigBase, ins: BaseModel, vlaue):
        self.config[row.key][ins.key] = vlaue

    def get_param_value(self, row: ConfigBase, ins: BaseModel):
        if ins.key not in self.config[row.key]:
            self.config[row.key][ins.key] = ins.default_value
        return self.config[row.key][ins.key]
