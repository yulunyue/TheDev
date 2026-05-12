from .model import BaseModel


class SearchModel(BaseModel):
    url = ""

    @classmethod
    def get_type(cls):
        return "search"

    def set_url(self, url):
        self.url = url
        return self

    def to_json(self):
        return super().to_json(url=self.url)
