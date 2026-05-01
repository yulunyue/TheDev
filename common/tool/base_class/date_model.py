from .base_model.model import BaseModel
from common.util.export import time_strptime, time_format
import time


class DateModel(BaseModel):
    def set_value(self, value: str):
        if value is None or not value:
            value = ""
        if not isinstance(value, str):
            value = time_format(value)
        return super().set_value(value)
