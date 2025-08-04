import json
from common.util.fp import File
from typing import List, Dict

CONFIG_SETTING_DIR = "data/setting"


class ConfigBase:

    def __init__(self) -> None:
        from common.tool.base_class.model import BaseModel

        self.fp: File = None
        self._params: Dict[str, BaseModel] = {}

        self.init_param()
        self.init()

    def set_resource(self, path):
        if isinstance(path, str):
            path = File(path)
        self.fp = path
        self.config = dict()
        if self.fp.exists():
            self.config.update(self.fp.read_file())
        return self

    def save(self, data):
        self.fp.write_file(data)
        return self

    def update_param_value(self, param, value):
        pass

    def get_param_value(self, param):
        return param.value

    def clone(self):
        ret = self.__class__()
        return ret

    def load(self, **kw):
        for key, value in self._params.items():
            if key in kw:
                value.set_value(kw[key])
        return self

    def init_param(self):
        pass

    def get_config(self) -> dict:
        return self.config

    def init(self):
        # self._config.update(self.get_config())
        from common.tool.base_class.model import BaseModel

        for key in dir(self):
            if key.startswith("_"):
                continue
            v = getattr(self, key)
            if not isinstance(v, BaseModel):
                continue
            self._params[key] = v.set_key(key).set_datasource(self)

    def to_json(self):
        return {v.key: v.get_value() for v in self._params.values()}
