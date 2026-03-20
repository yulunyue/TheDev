from .model import BaseModel


class BoolModel(BaseModel):
    ENABLE = "enable"
    DISABLE = "disable"

    def __init__(self, default_value=False, data_source=None, key=None):
        super().__init__(default_value=default_value, data_source=data_source, key=key)
