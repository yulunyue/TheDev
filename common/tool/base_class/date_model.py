from .base_model.model import BaseModel


def get_dates(value):
    if isinstance(value, str):
        value = [int(v) for v in value.replace(" ", "-").split("-") if v]
    if len(value) != 3:
        raise Exception(f"len(value)={len(value)} excepect 3")
    return value


class DateModel(BaseModel):
    def set_value(self, value):
        try:
            get_dates(value)
        except Exception as e:
            raise Exception(e, value, "yyyy-mm-dd")
        return super().set_value(value)
