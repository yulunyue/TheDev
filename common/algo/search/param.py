from typing import List, Dict
import numpy as np


class Param:
    def __init__(self, key):
        self.key = key
        self.args = None

    def set_args(self, args):
        self.args = args
        return self

    def load_value(self, min_value, max_value, value=None):
        self.value = value or (min_value + max_value) // 2
        self.min_value = min_value
        self.max_value = max_value
        return self

    def clone(self):
        return (
            self.__class__(self.key)
            .set_args(self.args)
            .load_value(self.min_value, self.max_value, self.value)
        )

    def get_value(self):
        return self.value

    def gen_value(self, step=None):
        if step == "random":
            self.value = np.random.randint(self.min_value, self.max_value)
        elif callable(step):
            self.value = step(self)
        elif step is None:
            pass
        elif 0 <= step <= 1:
            self.value = self.min_value + (self.max_value - self.min_value) * step
        return self


class Params:

    def __init__(self):
        self.score = 0

    def init_param(self):
        self._params: Dict[str, Param] = dict()
        for k in dir(self):
            if k.startswith("_"):
                continue
            p = getattr(self, k)
            if isinstance(p, Param):
                self._params[p.key] = p

    def get(self, key):
        return self._params.get(key)

    def clone(self, step=None):
        ret = self.__class__()
        ret._params = dict()
        for k, v in self._params.items():
            ret._params[k] = v.clone().gen_value(step)
        return ret

    def __str__(self):
        return str({key: self._params[key].get_value() for key in self._params})
