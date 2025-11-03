from common.third_util.c_profile import CProfileUtil
from common.util.export import ToolBase, Module


class Dfx(ToolBase):
    def cp(self, module_name, fun_name):
        def util():
            cls = Module().load_module(module_name, fun_name=fun_name)

            return cls().debug()

        CProfileUtil().run(util)


if __name__ == "__main__":
    Dfx().run()
