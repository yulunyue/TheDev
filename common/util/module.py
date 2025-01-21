import sys
from importlib import import_module, invalidate_caches
import os

class Module:
    def __init__(self) -> None:
        pass

    def load_module(self, module_name, path=None, fun_name=""):
        
        if path and path not in sys.path:
            sys.path.append(path)
        invalidate_caches()
        ret = import_module(module_name)

        if fun_name:
            for attr in fun_name.split('.'):
                ret = getattr(ret, attr)
        sys.modules.pop(module_name)
        # sys.path.pop()
        return ret
    
    def run(self,path,module_name,fun_name):
        old_pwd=os.getcwd()
        os.chdir(path)
        fn=self.load_module(module_name,fun_name)
        ret=fn()
        os.chdir(old_pwd)
        return ret
