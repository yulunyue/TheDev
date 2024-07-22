
from typing import List
import json


class BaseField:
    def __init__(self, **kwargs) -> None:
        self._keys: List[str] = []
        for k, v in kwargs.items():
            self.set_data(k, v)
        for key in dir(self):
            if key.startswith('_'):
                continue
            value = getattr(self, key)
            if callable(value):
                continue
            self._keys.append(key)

    def to_json(self):
        ret = dict()
        for key in self._keys:
            value = getattr(self, key)
            if hasattr(value, 'to_json'):
                value = value.to_json()
            ret[key] = value
        return ret

    def set_data(self, key, value):
        if key not in self._keys:
            self._keys.append(key)
        setattr(self, key, value)


class BaseModel:
    def __init__(self, value=None) -> None:
        self.value = value
        self.data_source = None
        self.key = ""

    def get_value(self) -> str:
        if self.data_source and self.key:
            ret = self.data_source.get_key_value(self.key)
            if ret is not None:
                self.value = ret
        return self.value


class StrModel(BaseModel):
    def __init__(self, value="") -> None:
        super().__init__(value)


class IntModel(BaseModel):
    def __init__(self, value) -> None:
        super().__init__(value)


class DictModel(BaseModel):
    def __init__(self, value=None) -> None:
        super().__init__(value or dict())

    def get(self, key, default_value=None) -> dict:
        if key in self.value:
            return self.value[key]
        self.value[key] = default_value
        return default_value

    def get_value(self) -> dict:
        return super().get_value()


ENABLE = "enable"
DISABLE = "disable"


class EnableModel(BaseModel):
    def __init__(self, value=DISABLE) -> None:
        super().__init__(value)

    def get_value(self):
        return super().get_value() == ENABLE


class EncroyModel(BaseModel):
    def get_value(self) -> str:
        return json.load(open('data/doc/password.json', 'r'))[self.value]
