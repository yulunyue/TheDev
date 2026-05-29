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
    Self,
)


class FileConfig(ConfigBase):

    @classmethod
    def init_resource(cls):
        cls.fp = File(cls.resource_path)
        cls.load_data_from_file()
        return cls.instance_map

    @classmethod
    def load_data_from_file(cls):
        has_update, cls._config = cls.fp.read_fast_file()
        if cls._config is None:
            cls._config = dict()
        if not has_update:
            return
        if not hasattr(cls, "instance_map") or cls.instance_map is None:
            cls.instance_map = dict()
        existing_keys = set(cls.instance_map.keys())
        new_keys = set(cls._config.keys())
        for k in existing_keys - new_keys:
            cls.instance_map.pop(k, None)
        for k, v in cls._config.items():
            try:
                if k not in cls.instance_map:
                    cls.insert(k, **v)
                else:
                    cls.instance_map[k].update(**v)
            except Exception as e:
                logger.error(e, stack_info=True)

    @classmethod
    def query(cls, key) -> Self:
        try:
            return cls.instance_map[key]
        except Exception as e:
            raise Exception(e, cls.resource_path)

    @classmethod
    def save_to_local(cls):
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

    def delete(self):
        self.instance_map.pop(self._id)
        self._config.pop(self._id)
        return self

    @classmethod
    def all(cls) -> List[Self]:
        return cls.instance_map.values()
