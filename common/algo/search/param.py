from typing import List, Dict
import numpy as np


class Param:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def clone(self, *args, **kw):
        return self.__class__(self.key, self.value)

    def get_value(self):
        return self.value


class Params:
    _params: Dict[str, Param] = None

    def get_params(self):
        if self._params is not None:
            return self._params
        self._params: Dict[str, Param] = dict()
        for k in dir(self):
            if k.startswith("_"):
                continue
            p = getattr(self, k)
            if isinstance(p, Param):
                if p.key is None:
                    p.key = k
                self._params[p.key] = p.clone()
        return self._params

    def clone(self, *args, **kw):
        params = self.get_params()
        for k in params:
            params[k] = params[k].clone(*args, **kw)
        return self
