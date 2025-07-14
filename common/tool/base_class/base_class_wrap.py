from common.util.log import logger


def set_value(v, b):
    if isinstance(v, BaseData):
        return v.set_value(b)
    return b


def get_value(v):
    if isinstance(v, BaseData):
        return v.get_value()
    return v


class BaseData:
    def __init__(self, key) -> None:
        self.key = key
        self.value = None
        self.init()

    def init(self):
        pass

    def set_value(self, value):
        if isinstance(value, BaseData):
            self.value = value.value
        else:
            self.value = value
        return self

    def get_value(self):
        return self.value

    def log(self, op, v, result):
        logger.info(f"{self} {op} {v}->{result}", stacklevel=2)

    def __ge__(self, value):
        ret = self.value > get_value(value)
        self.log(">", value, ret)
        return ret

    def __gt__(self, value):
        ret = self.value >= get_value(value)
        self.log(">=", value, ret)
        return ret

    def __neg__(self):
        self.log("-", self.value, -self.value)
        return self.__class__(self.key).set_value(-self.value)

    def __str__(self) -> str:
        return f"{self.key}:{self.value}"


class Number(BaseData):
    def init(self):
        self.value = 0
