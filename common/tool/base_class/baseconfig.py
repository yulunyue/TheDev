import json
from common.util.fp import File
from typing import List, Dict
from common.util.export import logger

CONFIG_SETTING_DIR = "config/setting"
from common.tool.base_class.model import BaseModel


class ConfigBase:
    _params_cls_map: Dict[str, BaseModel] = None
    _ins = dict()

    def __init__(self, key: str):
        self.key = key

    def load(self):
        self.params: Dict[str, BaseModel] = dict()
        for k, v in self.get_params().items():
            c = v.clone().set_datasource(self).set_key(k)
            setattr(self, k, c)
            self.params[k] = c
        self.init()

    @classmethod
    def get_headers_keys(cls):
        return cls.get_params().keys()

    # @classmethod
    # def new(cls, key, f=None):
    #     if key not in cls._ins:
    #         cls._ins[key] = cls(key).set_resource(f)
    #         cls._ins[key].save()
    #     return cls._ins[key]

    def init(self):
        pass

    def set_resource(self, resource: str):
        if isinstance(resource, str):
            if "/" not in resource:
                resource = CONFIG_SETTING_DIR + "/" + resource + ".json"
            resource = File.new(resource).write_if_not_exists(dict())
        self.load()
        self.resource: File = resource
        return self

    @classmethod
    def get_params(self):
        if self._params_cls_map is None:
            self.init_param()
        return self._params_cls_map

    @classmethod
    def to_web_view(self):
        return [
            dict(key=k, value=v.get_title(), type=v.get_type())
            for k, v in self.get_params().items()
        ]

    @classmethod
    def get_default_conifg(cls):
        ret = dict()
        for key, v in cls.get_params().items():
            ret[key] = v.default_value
        return ret

    def update_param_value(self, param, value):
        # logger.info([self.key, param.key, param, id(self), value])
        if self.resource:
            return self.resource.update_param_value(self, param, value)
        param.value = value

    resource: File = None

    def get_param_value(self, param):
        if self.resource is None:
            if param.value is None:
                param.value = param.default_value
            return param.value
        return self.resource.get_param_value(self, param)

    def update(self, **kw):

        for k, v in kw.items():
            if k in self.params:
                self.params[k].set_value(v)
        return self

    @classmethod
    def init_param(cls):
        from common.tool.base_class.model import BaseModel

        cls._params_cls_map = dict()
        for key in dir(cls):
            if key.startswith("_"):
                continue
            v = getattr(cls, key)
            if not isinstance(v, BaseModel):
                continue
            cls._params_cls_map[key] = v.set_key(key)
        return cls._params_cls_map

    def to_json(self):
        return {v.key: v.get_value() for v in self.params.values()}

    def save(self):
        if self.resource is None:
            return self
        cg = dict()
        if self.resource.exists():
            cg = self.resource.get_config()
        cg.update(self.to_json())
        logger.debug(self.resource)
        self.resource.write_file(cg)
        return self
