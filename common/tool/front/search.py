from common.util.export import Node, List, Dict, Any
from .util import FontBase


class FontSearch(FontBase):
    type = "search"

    def get_title(self):
        return self.title or self.value
