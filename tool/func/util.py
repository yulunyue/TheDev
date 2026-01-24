from common.third_util.c_profile import CProfileUtil
from common.util.export import logger, base64_encode, Module
from common.tool.export import PyUtil, ToolBase


class Dfx(ToolBase):
    def execute(self, module_name, fun_name):
        def util():
            ins: ToolBase = Module().load_module_object(module_name)()
            if hasattr(ins, "prepare"):
                ins.prepare()
            return getattr(ins, fun_name)()

        CProfileUtil().run(util)

    def pip_download(self, pkg):
        d = PyUtil().pip_download(pkg)
        logger.info(d)

    def b64_encode(self, code="print('hello world')"):
        logger.info(base64_encode(code))


if __name__ == "__main__":
    Dfx().run()
