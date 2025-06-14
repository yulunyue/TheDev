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

    RUN_TMP_PATH = "data/algo/run.py"

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

        def file_to_line(path, parent):
            path = mock_map.get(path, path)
            if path in vt_history:
                return vt_history[path]
            if parent is not None:
                vt_history[parent]["out_deg"] += 1
            vt_history[path] = dict(path=path, lines=[], out_deg=0, parent=parent)
            # paths = []
            lns = File(path).read_line()
            for ln in lns:
                if not ln:
                    continue
                if ln.strip().startswith("from"):
                    depend_path = ln.strip().split(" ")[1].replace(".", "/") + ".py"
                    for pre in prefix:
                        if depend_path.startswith(pre):
                            file_to_line(depend_path, path)
                            break
                    else:
                        vt_history[path]["lines"].append(ln)
                else:
                    vt_history[path]["lines"].append(ln)
            # vt_history[path]["depends"] = paths
            # logger.info(f'{path}, {parent},{vt_history[path]["out_deg"]}')
            return vt_history[path]

        lines = []
        file_to_line(src, None)

        q = [v for v in vt_history.values() if v["out_deg"] == 0]
        while q:
            t = q
            q = []
            for v in t:
                lines.extend(v["lines"])
                if v["parent"] is None:
                    continue
                vt_history[v["parent"]]["out_deg"] -= 1
                # logger.info(
                #     [v["path"], v["parent"], vt_history[v["parent"]]["out_deg"]]
                # )
                if vt_history[v["parent"]]["out_deg"] == 0:
                    q.append(vt_history[v["parent"]])
        File(dst).write_file("\n".join(lines))

    def compile_one(self, src, path=None):
        if path is None:
            path = self.RUN_TMP_PATH
        if not isinstance(src, str):
            src = inspect.getmodule(src).__file__
        self.megre_to_one(
            src,
            path,
            mock_map={
                "common/third_util/export.py": "common/mock.py",
                "common/util/export.py": "common/mock.py",
                "common/service/export.py": "common/mock.py",
                "common/algo/export.py": "common/mock.py",
            },
            prefix=["common", "app"],
        )
        return self.RUN_TMP_PATH
