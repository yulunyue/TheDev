from .model import BaseModel


class EncryptModel(BaseModel):
    @classmethod
    def get_type(cls):
        return "input"
