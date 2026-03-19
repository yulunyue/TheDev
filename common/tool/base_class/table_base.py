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


class FileConfig(ConfigBase):

    @classmethod
    def get_map_form_resource(cls):
        assert cls.resource_path
        cls.fp = File(cls.resource_path)
        cls.instance_map: Dict[str, ConfigBase] = dict()
        cls.idx = 0
        cls.config = cls.fp.read_file()
        if cls.fp.exists():
            for k, v in cls.config.items():
                t: ConfigBase = cls.insert(k)
                t.update(**v)
        else:
            cls.fp.write_file(dict())
        return cls.instance_map

    @classmethod
    def init_param(cls):
        super().init_param()
        cls.get_map_form_resource()

    @classmethod
    def insert(cls, idx=None):
        cls.idx += 1
        if idx is None:
            idx = self.idx
        cls.instance_map[idx] = cls(idx)
        return cls.instance_map[idx]

    @classmethod
    def get(cls, key):
        ins = cls.get_map_form_resource()
        if key in ins:
            return ins[key]
        ins[key] = cls.insert(key)
        return ins[key]

    @classmethod
    def save(cls):
        cls.fp.write_file(cls.config)
        return cls

    def update_param_value(self, ins: BaseModel, value):
        self.__class__.config[self._id][ins.key] = value

    def get_param_value(self, ins: BaseModel):
        # logger.map(key=row.key, k=ins.key)
        if self._id not in self.__class__.config:
            return ins.default_value
        c = self.__class__.config[self._id]
        if ins.key in c:
            return c[ins.key]
        return ins.default_value

    @classmethod
    def all(cls):
        return cls.get_map_form_resource().values()
