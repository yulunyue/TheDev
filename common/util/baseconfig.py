import json
from common.util.fp import File
from typing import List
from common.util.model import StrModel, BaseModel, EnableModel, EncroyModel, DictModel

CONFIG_SETTING_DIR = "data/setting"


class ConfigBase:

    def __init__(self, file_name, config_name) -> None:
        self._config_name = config_name
        self._fp = File(f"{CONFIG_SETTING_DIR}/{file_name}.json")
        self._mtime = 0
        self._params: List[BaseModel] = []
        self._config = dict()
        self.init_param()
        self.init()

    def add_param(self, param):
        self._params.append(param)

    def init_param(self):
        pass

    def save(self):
        self._fp.write_file(self._config)

    def get_config(self) -> dict:
        if self._fp.exists():
            self._config = self._fp.read_fast_file()
        return self._config

    def init(self):
        self._config = self.get_config()
        for key in dir(self):
            if key.startswith("_"):
                continue
            v = getattr(self, key)
            if not isinstance(v, BaseModel):
                continue
            v.key = key

    def get_key_value(self, key):
        config = self._config.get(self._config_name, self._config)
        return config.get(key)
