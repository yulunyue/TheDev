from ..base_model import BaseModel, StrModel, DictModel
from ..base_model.number_model import NumberModel
from ..baseconfig import ConfigBase
from common.util.export import (
    File,
    TypeVar,
    Generic,
    get_origin,
    get_args,
    logger,
    List,
    Dict,
    THE_DEV_CONSTANT,
)

T = TypeVar("T", bound="FileConfig")


class FileConfig(ConfigBase):

    @classmethod
    def init_resource(cls):
        assert cls.resource_path
        cls.fp = File(cls.resource_path)

        if cls.fp.exists():
            cls._config = cls.fp.read_file()
            items = list(cls._config.items())
            for k, v in items:
                cls.insert(k, **v)
        else:
            cls._config = dict()
        return cls.instance_map

    @classmethod
    def save(cls):
        cls.fp.write_file(cls._config)
        return cls

    def update_param_value(self, ins: BaseModel, value, if_none=False):
        c = self.__class__._config
        if self._id not in c:
            c[self._id] = dict()
        if ins.key in c[self._id] and if_none:
            return
        c[self._id][ins.key] = value

    def get_param_value(self, ins: BaseModel):
        # logger.map(key=row.key, k=ins.key)
        if self._id not in self.__class__._config:
            return ins.default_value
        c = self.__class__._config[self._id]
        if ins.key in c:
            return c[ins.key]
        return ins.default_value

    @classmethod
    def all(cls: T) -> List[T]:
        return cls.instance_map.values()
