from common.third_util.c_profile import CProfileUtil
from common.util.export import ToolBase, Module


class Dfx(ToolBase):
    def prepare(self, module_name, fun_name):
        self.module_name = module_name
        self.fun_name = fun_name

    def execute(self):
        def util():
            ins: ToolBase = Module().load_module_object(self.module_name)()
            if hasattr(ins, "prepare"):
                ins.prepare()
            return getattr(ins, self.fun_name)()

        CProfileUtil().run(util)


if __name__ == "__main__":
    Dfx().run()
