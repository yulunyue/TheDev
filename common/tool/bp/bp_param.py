from .node import BpNode


class BpParam(BpNode):
    def __init__(self, key, type, default_value=None):
        self.key = key
        self.type = type
        self.default_value = default_value
        super().__init__()

    def set_value(self, value):
        if isinstance(value, str):
            if self.type == "int":
                value = int(value)
            elif self.type == "float":
                value = float(value)
        return super().set_value(value)
