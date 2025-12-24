import json
from common.util.fp import File
from typing import List, Dict
from common.util.export import logger

CONFIG_SETTING_DIR = "config/setting"
from common.tool.base_class.model import BaseModel, StrModel


class ConfigBase:
    _params_cls_map: Dict[str, BaseModel] = None
    _ins = dict()

    def __init__(self, key: str):
        self.key = key
        self.params: Dict[str, BaseModel] = dict()
        for k, v in self._params_cls_map.items():
            c = v.clone().set_datasource(self).set_key(k)
            setattr(self, k, c)
            self.params[k] = c
        self.init()

    @classmethod
    def new(cls, key, f=None):
        if key not in cls._ins:
            cls._ins[key] = cls(key).set_resource(f)
            cls._ins[key].save()
        return cls._ins[key]

    def init(self):
        pass

    def set_resource(self, resource: str):
        if isinstance(resource, str):
            if "/" not in resource:
                resource = CONFIG_SETTING_DIR + "/" + resource + ".json"
            resource = File.new(resource).write_if_not_exists(dict())
        self.resource: File = resource
        return self

    def __new__(cls, *args):
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
        return {v.key: v.get_value() for v in self.params.values()}

    def save(self):
        cg = dict()
        if self.resource.exists():
            cg = self.resource.get_config()
        cg.update(self.to_json())
        logger.debug(self.resource)
        self.resource.write_file(cg)
        return self
