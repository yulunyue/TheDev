from typing import List, Dict
import json


class BaseModel:
    def __init__(self, key=None, default_value=None, data_source=None) -> None:
        self.default_value = default_value
        from common.tool.base_class.baseconfig import ConfigBase

        self.data_source: ConfigBase = data_source
        self.ops = []
        self.title = key
        self.key = key

    def clone(self):
        return self.__class__(key=self.key, default_value=self.default_value)

    def set_datasource(self, data_source):
        self.data_source = data_source
        return self

    def set_key(self, key):
        self.key = key
        if not self.title:
            self.title = self.key
        return self

    def get_value(self) -> str:
        if self.data_source is not None:
            return self.data_source.get_param_value(self)
        return self.default_value

    def set_value(self, value):
        return self.data_source.update_param_value(self, value)

    web_type = ""

    def to_web_view(self):
        return dict(
            type=self.web_type, value=self.value, defaullt_value=self.default_value
        )

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

    def __repr__(self) -> str:
        return f"key:{self.key}"


class StrModel(BaseModel):
    pass


class NumberModel(BaseModel):
    def get_value(self):
        try:
            return int(super().get_value())
        except Exception as e:
            raise e


def number(v):
    if isinstance(v, NumberModel):
        return v
    return NumberModel(v)


class DictModel(BaseModel):
    value: dict

    def __init__(self, key=None, default_value=None, data_source=None):
        super().__init__(key, default_value or dict(), data_source)

    def get_value(self) -> dict:
        return super().get_value()

    def update(self, **kw):
        return self.set_value(kw)


ENABLE = "enable"
DISABLE = "disable"


class EnableModel(BaseModel):
    def __init__(self, value=DISABLE) -> None:
        super().__init__(value)

    def get_value(self):
        return super().get_value().lower() in {ENABLE, "true"}


class EncroyModel(BaseModel):
    def get_value(self) -> str:
        return json.load(open("data/doc/password.json", "r"))[self.value]


if __name__ == "__main__":
    print(number(3) + 4 - 2)
