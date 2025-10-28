from common.util.export import (
    ToolBase,
    Module,
    defaultdict,
    logger,
    File,
    run_catch_error,
    get_log,
    List,
    Dict,
    Case,
)
from common.tool.export import ThreadRecord
from common.mock import MockCf
import json


def get_ins(file_name: str):
    if file_name.endswith(".py"):
        md = Module().load_module(f"app.yly.algo.context.{file_name[:-3]}")
        Module().compile_one(f"app/yly/algo/context/{file_name}")
        # logger.enable_cache()
        ins: MockCf = md.Solution()
        ins.dev = True
    elif file_name.endswith(".cpp"):
        pass
    return ins


class CaseMgmt:
    def __init__(self, file_name: str):
        self.root = File(f"data/context/{file_name.replace('.py','')}")
        self.root.child("case1").make_dir_if_not_exist(True)
        self.load()

    def load(self):
        self.cases: Dict[str, Case] = dict()
        for f in self.root.list_dir(with_dir=True):
            if f.is_dir():
                self.cases[f.name] = Case(f.path)

    def get_cases(self, name):
        if not name:
            return self.cases.values()
        return [self.cases[name]]


class ToolContext(ToolBase):

    def test(self, file_name, case_name=""):
        cm = CaseMgmt(file_name)
        ins: MockCf = get_ins(file_name)
        for case in cm.get_cases(case_name):
            ins.set_logger(case.get_loger())
            ins.set_inputs(case.get_linput_lines())
            f = getattr(ins, "execute")
            inp = case.get_input()
            r = f(**inp)
            msg = case.run_diff(r)
            if msg:
                logger.info(f"{case.i.path}\n{msg[:100]}")

    def debug(self):
        self.test("lc_399", "case1")


if __name__ == "__main__":
    ToolContext().run()
