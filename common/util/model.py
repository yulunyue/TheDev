from typing import List
import json


class BaseModel:
    def __init__(self, key, default_value=None, data_source=None) -> None:
        self.default_value = default_value
        from common.util.baseconfig import ConfigBase

        self.data_source: ConfigBase = data_source

        if self.data_source:
            self.data_source.add_param(self)
        self.ops = []
        self.key = key

    def get_value(self) -> str:
        if self.data_source and self.key:
            ret = self.data_source.get_key_value(self.key)
            if ret is not None:
                return ret
        return self.default_value

    def set_value(self, value):
        self.data_source.set_key_value(self.key, value)
        return self

    def __gt__(self, value):
        if isinstance(value, BaseModel):
            value = value.get_value()
        return self.get_value() < value

    def __sub__(self, value):
        if isinstance(value, BaseModel):
            value = value.get_value()
        self.value = self.value - value
        return self

    def __rsub__(self, value):
        if isinstance(value, BaseModel):
            value = value.get_value()
        self.value = value - self.value
        return self

    def __add__(self, value):
        if isinstance(value, BaseModel):
            value = value.get_value()
        self.value += value
        return self

    def __radd__(self, value):
        return self.__add__(value)

    def __str__(self) -> str:
        return f"value:{self.value},{self.ops}"


class StrModel(BaseModel):
    def __init__(self, key, data_source) -> None:
        super().__init__(key, data_source)


class NumberModel(BaseModel):
    def get_value(self):
        try:
            return int(super().get_value())
        except Exception as e:
            return None


def number(v):
    if isinstance(v, NumberModel):
        return v
    return NumberModel(v)


class DictModel(BaseModel):
    def __init__(self, key, data_source) -> None:
        super().__init__(key, data_source=data_source)

    def get(self, key, default_value=None) -> dict:
        store = self.get_value()
        if key in store:
            return store[key]
        return default_value

    def set(self, k, v):
        store = self.get_value()
        store[k] = v
        self.data_source.save()


ENABLE = "enable"
DISABLE = "disable"


class EnableModel(BaseModel):
    def __init__(self, value=DISABLE) -> None:
        super().__init__(value)

    def get_value(self):
        return super().get_value() == ENABLE


class EncroyModel(BaseModel):
    def get_value(self) -> str:
        return json.load(open("data/doc/password.json", "r"))[self.value]


if __name__ == "__main__":
    print(number(3) + 4 - 2)
