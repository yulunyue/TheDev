from common.util.export import (
    TestBase,
    Module,
    defaultdict,
    logger,
    File,
    run_catch_error,
    get_log,
    List,
    Dict,
)
from common.tool.export import ThreadRecord
from common.mock import MockCf
import json


def get_ins(file_name):
    md = Module().load_module(f"app.yly.algo.context.{file_name}")
    Module().compile_one(f"app/yly/algo/context/{file_name}.py")
    # logger.enable_cache()
    ins: MockCf = md.Solution()
    ins.dev = True
    return ins


class Case:
    def __init__(self, path):
        self.path = path
        self.i = File(path + "/main.in").write_if_not_exists()
        self.o = File(path + "/main.out").write_if_not_exists()
        self.e = File(path + "/main.e").write_if_not_exists()

    def get_loger(self):
        return get_log(self.path + "/main.log")

    def run_diff(self, result):
        self.o.write_file(result)
        e = None
        if self.e.exists():
            e = self.e.read_file()
        if str(e) == str(result):
            return ""
        return f"{result}!={e}"

    def get_input(self):
        data = self.get_linput_lines()
        try:
            return json.loads(data)
        except Exception as e:
            return dict()

    def get_linput_lines(self):
        return self.i.read_file()


class CaseMgmt:
    def __init__(self, file_name):
        self.root = File(f"data/context/{file_name}")
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


class TestContext(TestBase):

    def cases(self, file_name, fun_name="execute", case_name=""):
        cm = CaseMgmt(file_name)
        ins: MockCf = get_ins(file_name)
        for case in cm.get_cases(case_name):
            logger.info(case.i.path)
            ins.set_logger(case.get_loger())
            ins.set_inputs(case.get_linput_lines())
            r = getattr(ins, fun_name)(**case.get_input())
            self.expect(case.run_diff(r), "", case.path)

    def debug(self):
        self.cases("lg_p1209")


if __name__ == "__main__":
    TestContext().run()
