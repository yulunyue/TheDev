from common.util.export import Node


class FontBase(Node):
    type = "pre"


def to_web_view(k, v=None):
    if isinstance(v, FontBase):
        return v.set_key(k)
    if isinstance(k, dict):
        return k
    if isinstance(k, (str, int)):
        if v is None:
            v = k
        return dict(key=k, title=k, value=v, type="str")
    return k
