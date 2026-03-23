from common.util.export import Node, List, Dict, Any
from .util import FontBase


class FontSearch(FontBase):
    type = "search"

    @classmethod
    def get_dom_type(cls, v):
        return dict(title=v, value=dict(key=v))
