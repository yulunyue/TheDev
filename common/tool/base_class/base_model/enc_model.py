from .model import BaseModel


class EncroyModel(BaseModel):
    @classmethod
    def get_type(cls):
        return "input"

    def get_value(self) -> str:
        pass
