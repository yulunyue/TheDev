from .model import BaseModel


class DictModel(BaseModel):
    value: dict

    def __init__(self, default_value=None, data_source=None, key=None):
        super().__init__(
            default_value=default_value or dict(), data_source=data_source, key=key
        )

    def get(self, name, default_value=None):
        ret = self.get_value()
        if name not in ret and default_value is None:
            raise Exception(name, list(ret.keys()))
        return ret.get(name, default_value)

    def get_value(self) -> dict:
        return super().get_value()

    def update(self, **kw):
        return self.set_value(kw)

    def load(self, **kw):
        self._kw = kw
        return self

    @classmethod
    def get_type(cls):
        return "pre"
