from .base_model import BaseModel, StrModel, DictModel
from .number_model import NumberModel
from .baseconfig import ConfigBase
from ...constant import THE_DEV_CONSTANT
from common.util.export import (
    File,
    TypeVar,
    Generic,
    get_origin,
    get_args,
    logger,
    List,
    Dict,
)


class TableConfig(ConfigBase):
    pass


T = TypeVar("T")


class TableBase(Generic[T]):
    _concrete_type: ConfigBase = None

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
        logger.info(fp)
        self.config = dict()
        self.instance_map: Dict[str, ConfigBase] = dict()
        self.idx = 0
        if self.fp.exists():
            for k, v in self.fp.read_file().items():
                t: ConfigBase = self.insert(k)
                t.update(**v)
        else:
            self.fp.write_file(dict())
        return self

    def filter(self, **kw) -> List[T]:
        ret = []
        for k in self.config.keys():
            v: ConfigBase = self.get(k)
            # logger.map(v=id(v), k=k, key=v.key, d=v.to_json())
            ret.append(v)
        return ret

    def all(self):
        return self.filter()

    def insert(self, idx=None) -> T:
        self.idx += 1
        if idx is None:
            idx = self.idx
        return self.get(idx)

    def get(self, key) -> T:
        if key in self.instance_map:
            return self.instance_map[key]
        self.instance_map[key] = self._concrete_type(key)
        self.instance_map[key].set_resource(self)
        self.config[key] = dict()
        return self.instance_map[key]

    def save(self):
        self.fp.write_file(self.config)
        return self

    def update_param_value(self, row: ConfigBase, ins: BaseModel, value):
        # if row.key not in self.config:
        #     self.config[row.key] = dict()
        # logger.map(k1=row.key, k2=ins.key, v=value)
        self.config[row.key][ins.key] = value

    def get_param_value(self, row: ConfigBase, ins: BaseModel):
        # logger.map(key=row.key, k=ins.key)
        if ins.key not in self.config[row.key]:
            return ins.default_value
        return self.config[row.key][ins.key]
