from common.util.export import Node


class FontBase(Node):
    @classmethod
    def get_dom_type(cls, v, key=None, size=1):
        if isinstance(v, dict) or hasattr(v, "to_json"):
            return v
        return dict(key=v, value=v, title=v, type="str", size=size)
