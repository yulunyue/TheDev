import sys
import os
import inspect

from typing import List
from importlib import import_module, invalidate_caches

from common.util.fp import File
from common.util.log import get_log
from collections import defaultdict
import traceback

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


def run_catch_error(f, limit=0, **kw):
    try:
        res = f(**kw)
        return res
    except Exception as e:
        frame = inspect.currentframe()
        local_msgs = []
        while frame and limit:
            local_msgs.append(f"异常{frame.f_code.co_name}的局部变量:")
            for name, value in frame.f_locals.items():
                print(f"  {name} = {value}")
            frame = frame.f_back  # 回溯上一帧
            limit -= 1
        msgs = "\n".join(local_msgs)
        stacks_msgs = "".join(traceback.format_exception(e))
        return f"----stack----:{stacks_msgs}-------\n---locals---\n{msgs}\n----"


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

        mock_map = mock_map or dict()
        p = defaultdict(set)
        line_map = defaultdict(list)
        out = defaultdict(set)

        def file_to_line(path: str, vt: set):
            if path in out:
                return
            # paths = []
            out[path] = set()
            vt.add(path)
            lns = File(path).read_line()
            for ln in lns:
                if not ln:
                    continue
                if ln.strip().startswith("from"):
                    depend_path = ln.strip().split(" ")[1].replace(".", "/") + ".py"
                    depend_path: str = mock_map.get(depend_path, depend_path)
                    if depend_path in vt:
                        continue
                    for pre in prefix:
                        if depend_path.startswith(pre):
                            out[path].add(depend_path)
                            p[depend_path].add(path)
                            file_to_line(depend_path, vt)
                            break
                    else:
                        line_map[path].append(ln)
                else:
                    line_map[path].append(ln)
            vt.remove(path)

        lines = []
        file_to_line(src, set())
        q = [k for k, v in out.items() if len(v) == 0]
        # logger.map(p=p, out=out, q=q, indent=2)
        while q:
            t = q
            q = []
            for v in t:
                # logger.info(v)
                lines.extend(line_map[v])
                for u in p[v]:
                    out[u].remove(v)
                    # logger.map(v=v, u=u, o=out[u])
                    if len(out[u]) == 0:
                        q.append(u)
        File(dst).write_file("\n".join(lines))

    def compile_one(self, src, path=None):
        if path is None:
            path = self.RUN_TMP_PATH
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
