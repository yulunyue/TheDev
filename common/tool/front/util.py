from common.util.export import Node


class FontBase(Node):
    pass


def to_web_view(k, v):
    if isinstance(v, FontBase):
        return v.set_key(k)
    return dict(key=k, title=k, value=v, type="str")
