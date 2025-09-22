from common.util.export import get_log

logger = get_log("bp")


class BpNode:
    def __init__(self):
        self.value = None

    def set_value(self, value):
        self.value = value
        return self

    def get_value(self):
        if hasattr(self.value, "get_value"):
            return self.value.get_value()
        return self.value
