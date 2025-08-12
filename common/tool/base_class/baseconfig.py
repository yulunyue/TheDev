import json
from common.util.fp import File
from typing import List, Dict

CONFIG_SETTING_DIR = "data/setting"
from common.tool.base_class.model import BaseModel, StrModel


class ConfigBase:
    _params_cls_map: Dict[str, BaseModel] = None

    def __init__(self, key):
        self.key = key
        self.params = dict()
        for k, v in self._params_cls_map.items():
            c = v.clone().set_datasource(self).set_key(k)
            setattr(self, k, c)
            self.params[k] = c

    def set_resource(self, resource):
        self.resource = resource
        return self

    def __new__(cls, *args) -> None:
        cls.init_param()
        return super().__new__(cls)

    @classmethod
    def get_params(cls):
        if cls._params_cls_map is None:
            cls.init_param()
        return cls._params_cls_map

    @classmethod
    def get_default_conifg(cls):
        ret = dict()
        for key, v in cls.get_params().items():
            ret[key] = v.default_value
        return ret

    def update_param_value(self, param, value):
        return self.resource.update_param_value(self, param, value)

    def get_param_value(self, param):
        return self.resource.get_param_value(self, param)

    def update(self, **kw):
        for k, v in kw.items():
            self.params[k].set_value(v)
        return self

    @classmethod
    def init_param(cls):
        # self._config.update(self.get_config())
        from common.tool.base_class.model import BaseModel

        cls._params_cls_map = dict()
        for key in dir(cls):
            if key.startswith("_"):
                continue
            v = getattr(cls, key)
            if not isinstance(v, BaseModel):
                continue
            cls._params_cls_map[key] = v.set_key(key)

    def to_json(self):
        return {v.key: v.get_value() for v in self._params.values()}
