class ListUtil:
    def __init__(self, array: list):
        self.array = array

    def get_one(self, func, get_value=None):
        if get_value is None:
            get_value = lambda a: a
        ret_idx, ret_value = None, None
        for i, v in enumerate(self.array):
            if ret_value is None or func(get_value(v), get_value(ret_value)):
                ret_idx, ret_value = i, v
        return ret_idx, ret_value

    def max(self, fn=None):
        return self.get_one(lambda a, b: a > b, fn)

    def min(self, fn=None):
        return self.get_one(lambda a, b: a < b, fn)

    def filter(self, fn):
        return [a for a in self.array if fn(a)]
