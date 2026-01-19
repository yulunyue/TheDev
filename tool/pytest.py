from common.third_util.py_test_util import PyTestUtil
from common.util.export import logger, base64_encode, File, SYS_ARGS
from common.tool.export import PyUtil, ToolBase


def make_test(f: File):
    s = "tests/" + f.path.replace(f.file_name, f"test_{f.file_name}")
    name = f.name.title()
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
    return ret.path


def files(root, name):
    return File(root).list_dir(depth=8, mathchs=[name], ignores=[".*__pycache__"])


class PyTest(ToolBase):

    def coverage(self):
        PyTestUtil().set_aim("tests").coverage()

    def test(self, key: str):

        if key:
            name, *args = key.split("::")
            taget = files("tests", name)
            if not taget:
                app_commons = files("app", name) + files("common", name)
                if len(app_commons) == 0:
                    raise Exception(key)
                elif len(app_commons) > 1:
                    for d in app_commons:
                        logger.info(d)
                    return
                else:
                    taget_src = app_commons[0]
                taget = [make_test(taget_src)]
            if args:
                if len(taget) != 1:
                    raise Exception(key, taget)
                taget = ["::".join([taget[0].path] + args)]
        else:
            taget = ["tests"]
        PyTestUtil().set_aim(*taget).coverage()


if __name__ == "__main__":
    PyTest().run()
