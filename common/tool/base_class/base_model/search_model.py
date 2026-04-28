from .model import BaseModel


class SearchModel(BaseModel):
    def __init__(self, default_value=None, key=None, data_source=None) -> None:
        super().__init__(default_value, key, data_source)
        self.url = ""

    @classmethod
    def get_type(cls):
        return "search"

    def set_url(self, url):
        self.url = url
        return self

    def to_json(self):
        return super().to_json(url=self.url)
