import sys
import os
import inspect

from typing import List, Dict
from importlib import import_module, invalidate_caches

from common.util.fp import File
from common.tool.str_util import StrUtil
from common.util.log import get_log, logger
from collections import defaultdict
import traceback


class FunInfo:
    def load(self, name, doc, args, kw, has_args, has_kw, has_self):
        self.name = name
        self.doc = doc
        self.args = args
        self.kw: dict = kw
        self.has_args = has_args
        self.has_kw = has_kw
        self.has_self = has_self
        return self

    def to_json(self):
        childs = []  # 前端需要这样的childs 数组
        for key in sorted(self.kw.keys()):
            v: dict = self.kw[key]
            v.update(key=key)
            childs.append(v)
        return dict(key=self.name, title=self.name, childs=childs)


def check_func_arg_kw(v):
    has_args = False
    has_kw = False
    p_or_k_ct = p_ct = k_ct = 0
    sig = inspect.signature(v)
    for param in sig.parameters.values():
        if param.kind == param.VAR_POSITIONAL:
            has_args = True
        elif param.kind == param.VAR_KEYWORD:
            has_kw = True
        elif param.kind == param.KEYWORD_ONLY:
            k_ct += 1
        elif param.kind == param.POSITIONAL_ONLY:
            p_ct += 1
        elif param.kind == param.POSITIONAL_OR_KEYWORD:
            p_or_k_ct += 1
        else:
            raise Exception(param)

    return p_or_k_ct, p_ct, k_ct, has_args, has_kw


def call_func_auto(func, *args, **kw):
    info = get_function_info(func)
    if info.has_args and info.has_kw:
        return func(*args, **kw)
    elif info.has_args:
        return func(*args)
    elif info.has_kw:
        return func(**kw)
    return func(*args[: len(info.args)])


def get_file_path_by_cls(cls):
    return inspect.getsourcefile(cls)


def get_function_info(v):
    argspec = inspect.getfullargspec(v)
    has_self = False
    df = argspec.defaults
    kgs = []
    if df is None:
        args = argspec.args
    else:
        args, kgs = argspec.args[0 : -len(df)], argspec.args[len(df) + 1 :]
    kw = dict()

    def a_help(key, default_value, is_pos):
        cls = argspec.annotations.get(key, None)
        ret = dict(title=key, default_value=default_value, type=None, is_pos=is_pos)

        if hasattr(cls, "type_info"):
            ret.update(cls.type_info)
        elif cls is not None:
            ret.update(type=cls.__name__)
        elif default_value is not None:
            ret.update(type=default_value.__class__.__name__)
        return ret

    ag = []
    for a in args:
        if a == "self":
            has_self = True
            continue
        ag.append(a)
        kw[a] = a_help(a, None, True)
    try:
        for i in range(len(kgs)):
            if i < len(df):
                kw[kgs[i]] = a_help(kgs[i], df[i], False)
            else:
                kw[kgs[i]] = a_help(kgs[i], None, False)
    except Exception as e:
        raise Exception(kw, kgs, df, e)
    p_or_k_ct, p_ct, k_ct, has_args, has_kw = check_func_arg_kw(v)
    return FunInfo().load(v.__name__, v.__doc__, ag, kw, has_args, has_kw, has_self)


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
        if path:
            sys.path.append(path)
        invalidate_caches()
        ret = md = import_module(module_name)

        if fun_name:
            for attr in fun_name.split("."):
                ret = getattr(ret, attr)
        sys.modules.pop(module_name)
        if path:
            sys.path.pop()  # 同名插件
        return ret

    def load_module_object(self, module_name: str, path: str = None):
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
        logger.info(File(dst).write_file("\n".join(lines)))

    def compile_one(self, src, path=None):
        if path is None:
            path = self.RUN_TMP_PATH
        mock_py = "common/mock.py"
        self.megre_to_one(
            src,
            path,
            mock_map={
                "common/third_service/oj.py": mock_py,
                "common/third_util/export.py": mock_py,
                "common/util/export.py": mock_py,
                "common/service/export.py": mock_py,
                "common/algo/export.py": mock_py,
            },
            prefix=["common", "app"],
        )
        return self
