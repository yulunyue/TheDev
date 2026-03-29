from .model import BaseModel


class ListModel(BaseModel):
    value: list

    def __init__(self, default_value=None, data_source=None, key=None):
        default_value = default_value or []
        super().__init__(default_value=default_value, key=key, data_source=data_source)

    def get_value(self) -> list:
        return super().get_value()

    def append(self, v):
        self.get_value().append(v)
        return self
