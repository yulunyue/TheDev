from .model import BaseModel


class NumberModel(BaseModel):
    def __init__(self, default_value=None, key=None, data_source=None):
        super().__init__(default_value=default_value, key=key, data_source=data_source)

    def set_value(self, value):
        if not isinstance(value, (float, int)):
            try:
                value = float(value)
            except Exception as e:
                raise Exception(e, value)
        return super().set_value(value)
