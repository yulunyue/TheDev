import sys

from common.exception import ValidationError

_AUTO_COUNTERS = {}


def auto(v=None):
    frame = sys._getframe(1)
    key = frame.f_code.co_name
    if key not in _AUTO_COUNTERS:
        _AUTO_COUNTERS[key] = 0
    if v is not None:
        _AUTO_COUNTERS[key] = v
    ret = _AUTO_COUNTERS[key]
    _AUTO_COUNTERS[key] += 1
    return ret


def auto_reset(name=""):
    if name:
        _AUTO_COUNTERS.pop(name, None)
    else:
        _AUTO_COUNTERS.clear()


class EnumCls:
    def __init__(self):
        cls = type(self)
        if "_value_to_name" not in cls.__dict__:
            mapping = {}
            for name in dir(self):
                if name.startswith("_"):
                    continue
                v = getattr(self, name)
                if isinstance(v, (int, str)):
                    mapping[v] = name
            cls._value_to_name = mapping

    def to_str(self, v):
        try:
            return self._value_to_name[v]
        except KeyError:
            raise ValidationError(
                "Invalid enum value",
                context={
                    "value": v,
                    "valid": list(self._value_to_name.keys()),
                },
            )

    def from_str(self, name):
        for v, n in self._value_to_name.items():
            if n == name:
                return v
        raise ValidationError(
            "Invalid enum name",
            context={
                "name": name,
                "valid": list(self._value_to_name.values()),
            },
        )

    def values(self):
        return list(self._value_to_name.keys())

    def names(self):
        return list(self._value_to_name.values())

    def items(self):
        return list(self._value_to_name.items())

    def __contains__(self, v):
        try:
            return v in self._value_to_name
        except TypeError:
            return False

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._value_to_name}>"
