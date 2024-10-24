import sys
from importlib import import_module


class Module:
    def __init__(self) -> None:
        pass

    def load_module(self, modeule_name, path=None, fun_name=""):
        if path and path not in sys.path:
            sys.path.append(path)
        ret = import_module(modeule_name)
        if fun_name:
            for attr in fun_name.split('.'):
                ret = getattr(ret, attr)
        sys.path.pop()
        return ret
