import sys
import os
import inspect

from typing import List, Dict
from importlib import import_module, invalidate_caches

from common.util.fp import File
from common.util.str_util import StrUtil
from common.util.log import get_log, logger
from collections import defaultdict
import traceback


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

    def a_help(key, default_value):
        cls = argspec.annotations.get(key, None)
        ret = dict(key=key, default_value=default_value, type=None)
        if hasattr(cls, "type_info"):
            ret.update(cls.type_info)
        elif cls is not None:
            ret.update(type=cls.__name__)
        return ret

    from common.service.export import Node

    return Node(
        key=v.__name__,
        title=v.__name__,
        data=dict(
            doc=v.__doc__,
            args=args,
            # annotated=str(v.__annotations__),
            kwargs={k: a_help(k, v) for k, v in kg.items()},
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

    def load_module_object(self, module_name: str, path: str):
        rpaths = module_name.replace("/", ".").split(".")
        object_name = rpaths.pop()
        return self.load_module(".".join(rpaths), path=path, fun_name=object_name)

    def run(self, path, module_name, fun_name):
        old_pwd = os.getcwd()
        os.chdir(path)
        fn = self.load_module(module_name, fun_name)
        ret = fn()
        os.chdir(old_pwd)
        return ret

    def megre_to_one(self, src, dst, mock_map: dict, prefix: List[str]):
        str_util = StrUtil().set_prefix(prefix)

        class Node:
            def __init__(self, path: str, vt: set):
                self.fp = File(path)
                self.lines = []
                self.childs: Dict[str, Node] = dict()
                self.out_deg = 0
                self.init(vt)

            def init(self, vt):
                for ln2 in self.fp.read_line():
                    if not ln2:
                        continue
                    ln = ln2.strip()
                    if ln2.strip().startswith("from"):
                        ln = ln2.strip().split(" ")[1]
                        if ln.startswith("."):
                            ln = self.fp.get_relative_path(ln)
                        if not str_util.str_prefix_match(ln):
                            self.lines.append(ln2)
                            continue
                        path = ln.replace(".", "/") + ".py"
                        if path in vt:
                            continue
                        p = file_to_line(path, vt)
                        if p is not None:
                            self.add_depends(p)
                    else:
                        self.lines.append(ln2)

            def add_depends(self, p: "Node"):
                if self.fp.path in p.childs:
                    return
                p.childs[self.fp.path] = self
                self.out_deg += 1

            def __repr__(self):
                return f"{self.fp.path} {list(self.childs.keys())} {self.out_deg}"

        nodes: Dict[str, Node] = dict()

        def file_to_line(path: str, vt: set):
            path = mock_map.get(path, path)
            if path in vt:
                return
            vt.add(path)
            if path not in nodes:
                nodes[path] = Node(path, vt)
            vt.remove(path)
            return nodes[path]

        lines = []
        file_to_line(src, set())
        q = [v for v in nodes.values() if v.out_deg == 0]
        while q:
            t = q
            q = []
            for v in t:
                # logger.debug(v)
                lines.extend(v.lines)
                for u in v.childs.values():
                    u.out_deg -= 1
                    if u.out_deg == 0:
                        q.append(u)
        File(dst).write_file("\n".join(lines))

    def compile_one(self, src, path=None):
        if path is None:
            path = self.RUN_TMP_PATH
        mock_py = "common/mock.py"
        self.megre_to_one(
            src,
            path,
            mock_map={
                "common/third_util/export.py": mock_py,
                "common/util/export.py": mock_py,
                "common/service/export.py": mock_py,
                "common/algo/export.py": mock_py,
            },
            prefix=["common", "app"],
        )
        return self
