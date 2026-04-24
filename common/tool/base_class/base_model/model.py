from common.util.export import List, TypeVar

T = TypeVar("T", bound="BaseModel")


class BaseModel:
    value = None

    def __init__(self, default_value=None, key=None, data_source=None) -> None:
        self.default_value = default_value
        from common.tool.base_class.baseconfig import ConfigBase

        self.value = default_value
        self.data_source: ConfigBase = data_source
        self.ops = []
        self.title = key
        self.key = key
        self.model: T = None
        self.visible = True

    def set_model(self, model):
        self.model: T = model
        return self

    def get_title(self):
        return self.title or self.key

    @classmethod
    def get_type(cls):
        return cls.__name__

    def clone(self):
        return self.__class__(key=self.key, default_value=self.default_value).set_model(
            self
        )

    def set_datasource(self, data_source):
        self.data_source = data_source
        return self

    def set_key(self, key):
        self.key = key
        if not self.title:
            self.title = self.key
        return self

    def get_value(self) -> str:
        value = None
        if self.data_source is not None:
            value = self.data_source.get_param_value(self)
        if value is None:
            value = self.default_value
        return value

    def set_value(self, value):
        return self.data_source.update_param_value(self, value)

    def set_value_if_none(self, value):
        return self.data_source.update_param_value(self, value, if_none=True)

    def to_json(self, **kw):
        v = self.get_value()
        ret = dict(
            type=self.get_type(),
            key=self.key,
            value=v,
            title=self.get_title(),
            visible=self.visible,
        )
        ret.update(kw)
        return ret

    def set_visible(self, visible: bool):
        self.visible = visible
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

    def __repr__(self) -> str:
        return f"{self.key}"
