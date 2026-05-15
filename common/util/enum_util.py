GLOBAL_ADD = 0

from common.exception import ValidationError


class EnumCls:
    def __init__(self):
        self._format = dict()
        for name in dir(self):
            if name.startswith("_"):
                continue
            v = getattr(self, name)
            if isinstance(v, (int, str)):
                self._format[v] = name

    def to_str(self, v):
        try:
            return self._format[v]
        except Exception as e:
            raise ValidationError("Invalid enum value", context={"format": self._format, "value": v})


def auto(v=None):
    global GLOBAL_ADD
    if v is not None:
        GLOBAL_ADD = v
    ret, GLOBAL_ADD = GLOBAL_ADD, GLOBAL_ADD + 1
    return ret
