import sys
import os
import inspect

from typing import List, Dict
from importlib import import_module, invalidate_caches
from .str_util import StrUtil
import traceback
from common.exception import ModuleLoadError


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
        childs = []  # 前端需要这样的children 数组

        for key in sorted(self.kw.keys()):
            v: dict = self.kw[key]
            v.update(key=key)
            childs.append(v)
        return dict(key=self.name, title=self.name, children=childs)


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
            raise ModuleLoadError("Unknown parameter kind", context={"param": param.kind})

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
        args, kgs = argspec.args[0 : -len(df)], argspec.args[len(df) :]
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
        raise ModuleLoadError("Failed to process function arguments", context={"kw": kw, "kgs": kgs, "defaults": df, "error": e})
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

    def __init__(self, use_cache=False) -> None:
        self.use_cache = use_cache

    def load_module(self, module_name, path=None):
        if path:
            sys.path.append(path)
        if not self.use_cache:
            invalidate_caches()
        ret = import_module(module_name)
        if not self.use_cache:
            sys.modules.pop(module_name)
        if path:
            sys.path.pop()  # 同名插件
        return ret

    def load_module_object(self, src: str, path: str = None):
        module_name, *names = src.split("::")
        if module_name.endswith(".py"):
            module_name = module_name[:-3]
        module_name = module_name.replace("/", ".")
        try:
            md = self.load_module(module_name, path=path)
            if not names:
                return md
            obj = getattr(md, names[0])
            for name in names[1:]:
                obj = getattr(obj, name)
            return obj
        except Exception as e:
            raise ModuleLoadError("Failed to load module object", context={"error": e, "src": src, "path": path, "module": module_name})
        raise ModuleLoadError("Invalid module path format", context={"src": src})

    def load_fun_call(self, path: str):
        if "?" in path:
            root_path, module_path = path.split("?")
        else:
            root_path, module_path = None, path
        return self.load_module_object(module_path, root_path)
