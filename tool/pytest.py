from common.third_util.py_test_util import PyTestUtil
from common.util.export import logger, base64_encode, File, SYS_ARGS, List, Module
from common.tool.export import PyUtil, ToolBase


def make_test(f: File):
    s = "tests/" + f.path.replace(f.file_name, f"test_{f.file_name}")
    name = f.name.title().replace("_", "")
    model_path = f.path.replace("/", ".").replace(".py", "")
    ret = File(s).write_if_not_exists(
        f"""
from common.util.export import TestBase, logger
from {model_path} import {name}


class Test{name}(TestBase):
    pass
"""
    )
    logger.info(ret)
    return ret


def files(root, name):
    return File(root).list_dir(depth=8, mathchs=[name], ignores=[".*__pycache__"])


def get_exe_by_key(name):
    taget = files("tests", name)
    if not taget:
        app_commons = files("app", name) + files("common", name)
        if len(app_commons) != 1:
            raise Exception(app_commons)
        else:
            taget_src = app_commons[0]
        taget = [make_test(taget_src)]
    return taget


class PyTest(ToolBase):

    def cover(self):
        PyTestUtil().set_aim("tests").coverage()

    def test(self, key: str, fun_name=""):
        taget: List[str] = [
            (f.path + "::" + fun_name) if fun_name else f for f in get_exe_by_key(key)
        ]
        PyTestUtil().set_aim(*taget).main()

    def exec(self, key: str, fun_name):
        fun_name = fun_name.split("::")
        for f in get_exe_by_key(key):
            module_name = f.path.replace(".py", "").replace("/", ".")
            md = Module().load_module(module_name)
            cls = getattr(md, fun_name[0], None)
            if cls is None:
                logger.error([f.path, fun_name])
                continue
            if hasattr(cls, "setup_class") and not getattr(cls, "setup_class_flag"):
                cls.setup_class()
                cls.setup_class_flag = True
            getattr(cls(), fun_name[1])()


if __name__ == "__main__":
    PyTest().run()
