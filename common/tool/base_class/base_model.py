from .model import BaseModel


class StrModel(BaseModel):
    @classmethod
    def get_type(cls):
        return "str"

    def __init__(self, default_value="", key=None, data_source=None):
        super().__init__(default_value=default_value, key=key, data_source=data_source)


class BoolModel(BaseModel):
    def __init__(self, default_value=False, data_source=None, key=None):
        super().__init__(default_value=default_value, data_source=data_source, key=key)


class ListModel(BaseModel):
    value: list

    def __init__(self, default_value=None, data_source=None, key=None):
        default_value = default_value or []
        super().__init__(default_value=default_value, key=key, data_source=data_source)

    def get_value(self) -> list:
        return super().get_value()


class DictModel(BaseModel):
    value: dict

    def __init__(self, default_value=None, data_source=None, key=None):
        super().__init__(
            default_value=default_value or dict(), data_source=data_source, key=key
        )

    def get_value(self) -> dict:
        return super().get_value()

    def update(self, **kw):
        return self.set_value(kw)


ENABLE = "enable"
DISABLE = "disable"


class EnableModel(BaseModel):
    def __init__(self, value=DISABLE) -> None:
        super().__init__(default_value=value)

    def get_value(self):
        return super().get_value().lower() in {ENABLE, "true"}


class EncroyModel(BaseModel):
    def get_value(self) -> str:
        pass
