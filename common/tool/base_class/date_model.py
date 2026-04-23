from .base_model.model import BaseModel


class DateModel(BaseModel):
    def set_value(self, value):
        return super().set_value(value)
