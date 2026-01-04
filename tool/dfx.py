from common.third_util.c_profile import CProfileUtil
from common.util.export import ToolBase, Module


class Dfx(ToolBase):
    def execute(self, module_name, fun_name):
        def util():
            ins: ToolBase = Module().load_module_object(module_name)()
            if hasattr(ins, "prepare"):
                ins.prepare()
            return getattr(ins, fun_name)()

        CProfileUtil().run(util)


if __name__ == "__main__":
    Dfx().run()
