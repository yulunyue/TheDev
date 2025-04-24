import sys
import os
import inspect

from typing import List
from importlib import import_module, invalidate_caches

from common.util.fp import File
from common.util.log import get_log


logger = get_log("module")


def get_function_info(v):
    argspec = inspect.getfullargspec(v)
    kg = {}
    if argspec.defaults is None:
        args = argspec.args
    else:
        df = argspec.defaults
        args = argspec.args[0 : -len(df)]
        kg.update(dict(zip(argspec.args[-len(df) :], df)))
    for a in args:
        if a == "self":
            continue
        kg[a] = None
    from common.service.export import Node

    return Node(
        key=v.__name__,
        title=v.__name__,
        data=dict(
            doc=v.__doc__,
            args=args,
            # annotated=str(v.__annotations__),
            kwargs=kg,
            # code=str(v),
        ),
    )


class Module:
    def __init__(self) -> None:
        pass

    def load_module(self, module_name, path=None, fun_name=""):
        if path and path not in sys.path:
            logger.info(f"add path {path}")
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
