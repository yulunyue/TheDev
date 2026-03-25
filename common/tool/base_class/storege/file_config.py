from ..base_model import BaseModel, StrModel, DictModel
from ..base_model.number_model import NumberModel
from ..extern_cls.front import FrontExtern
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


class FileConfig(FrontExtern):

    @classmethod
    def init_resource(cls):
        assert cls.resource_path
        cls.fp = File(cls.resource_path)

        if cls.fp.exists():
            cls.config = cls.fp.read_file()
            items = list(cls.config.items())
            for k, v in items:
                t: FileConfig = cls.insert(**v)
        else:
            cls.config = dict()
        return cls.instance_map

    @classmethod
    def save(cls):
        cls.fp.write_file(cls.config)
        return cls

    def update_param_value(self, ins: BaseModel, value):
        c = self.__class__.config
        if self._id not in c:
            c[self._id] = dict()
        c[self._id][ins.key] = value

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
        return cls.instance_map.values()
