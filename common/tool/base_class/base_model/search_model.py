from .model import BaseModel


class SearchModel(BaseModel):
    @classmethod
    def get_type(cls):
        return "search"

    def to_json(self):
        return super().to_json()
