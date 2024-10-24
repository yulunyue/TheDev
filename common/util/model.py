
from typing import List
import json


class BaseModel:
    def __init__(self, data_source, value=None) -> None:
        self.value = value
        self.data_source = data_source
        if self.data_source:
            self.data_source.add_param(self)
        self.key = ""

    def get_value(self) -> str:
        if self.data_source and self.key:
            ret = self.data_source.get_key_value(self.key)
            if ret is not None:
                self.value = ret
        return self.value

    def set_value(self, value):
        self.data_source.set_key_value(self.key, value)
        return self


class StrModel(BaseModel):
    def __init__(self, data_source, value="") -> None:
        super().__init__(data_source, value)


class IntModel(BaseModel):
    def __init__(self, data_source, value) -> None:
        super().__init__(data_source, value)


class DictModel(BaseModel):
    def __init__(self, data_source, value=None) -> None:
        super().__init__(data_source, value or dict())

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
