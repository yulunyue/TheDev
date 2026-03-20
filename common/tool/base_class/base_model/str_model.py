from .model import BaseModel


class StrModel(BaseModel):
    @classmethod
    def get_type(cls):
        return "input"

    def __init__(self, default_value="", key=None, data_source=None):
        super().__init__(default_value=default_value, key=key, data_source=data_source)
