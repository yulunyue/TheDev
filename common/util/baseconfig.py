import json
import os

from .model import StrModel, BaseModel, EnableModel, EncroyModel
from hcso_tool.utils.tool import write_file,log


class ConfigBase:
    def __init__(self) -> None:
        self._save_path = f'config/setting/{self.__class__.__name__}.json'
        self._mtime = 0
        self.init()

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(*args, **kwargs)
        return cls._instance

    def save(self, data):
        write_file(self._save_path, json.dumps(
            data, indent=4
        ))

    def get_config(self) -> dict:
        config = dict()
        if not os.path.exists(self._save_path):
            return config
        with open(self._save_path, 'r',encoding='utf-8') as f:
            config = json.load(f)
        return config

    def init(self):
        write_flag = False
        config_default = self.get_config()
        for key in dir(self):
            if key.startswith("_"):
                continue
            v = getattr(self, key)
            if not isinstance(v, BaseModel):
                continue
            if v.data_source is not None:
                log(f"repeat init {v.key} {self}")
            v.key = key
            v.data_source = self
            if key in config_default:
                v.value = config_default[key]
            else:
                write_flag = True
                config_default[key] = v.value
        if write_flag:
            self.save(config_default)

    def get_key_value(self, key):
        if not os.path.exists(self._save_path):
            return
        m_time = os.path.getmtime(self._save_path)
        if self._mtime == m_time:
            return
        self._mtime = m_time
        return self.get_config().get(key)