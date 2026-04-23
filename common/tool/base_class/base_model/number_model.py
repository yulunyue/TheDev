from .model import BaseModel


class NumberModel(BaseModel):
    def __init__(self, default_value=None, key=None, data_source=None):
        super().__init__(default_value=default_value, key=key, data_source=data_source)

    def set_value(self, value):
        if value is None or value == "undefined" or value == "":
            return super().set_value(self.default_value)
        if not isinstance(value, (float, int)):
            try:
                value = float(value)
            except Exception as e:
                return super().set_value(self.default_value)
        return super().set_value(value)

    @classmethod
    def get_type(cls):
        return "number"
