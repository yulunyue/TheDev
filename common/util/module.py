import sys
from importlib import import_module, invalidate_caches
import os
from common.util.fp import File
from common.util.log import get_log
from typing import List

logger = get_log("module")


class Module:
    def __init__(self) -> None:
        pass

    def load_module(self, module_name, path=None, fun_name=""):

        if path and path not in sys.path:
            sys.path.append(path)
        invalidate_caches()
        ret = import_module(module_name)

        if fun_name:
            for attr in fun_name.split("."):
                ret = getattr(ret, attr)
        sys.modules.pop(module_name)
        # sys.path.pop()
        return ret

    def run(self, path, module_name, fun_name):
        old_pwd = os.getcwd()
        os.chdir(path)
        fn = self.load_module(module_name, fun_name)
        ret = fn()
        os.chdir(old_pwd)
        return ret

    def megre_to_one(self, src, dst, mock_map: dict = None, prefix=None):
        vt_history = dict()
        mock_map = mock_map or dict()
        prefix = prefix or []

        def line_to_line(lns: List[str], parents):
            ret = []
            for ln in lns:
                if not ln:
                    continue
                if ln.startswith("from"):
                    path = ln.split(" ")[1].replace(".", "/") + ".py"
                    for pre in prefix:
                        if path.startswith(pre):
                            ret.extend(file_to_line(path, parents))
                            break
                    else:
                        ret.append(ln)
                else:
                    ret.append(ln)
            return ret

        def file_to_line(path, parents):
            path = mock_map.get(path, path)
            if path in vt_history:
                return []
            logger.info(f"{path}, {parents}")
            vt_history[path] = True
            return line_to_line(File(path).read_line(), parents + [path])

        lines = file_to_line(src, [])
        File(dst).write_file("\n".join(lines))
