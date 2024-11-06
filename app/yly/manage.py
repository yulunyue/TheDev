from common.tool.thread_util import run_watch_fun
from common.service.http import Node, http_test

from common.util.module import Module
from common.util.log import logger
from common.util.fp import File
import os
import time
import sys
import json


class SolutionBase:
    logs = []
    case_load = None
    name = "test"

    def __init__(self) -> None:
        self.watch_var = []

    def get_cases(self):
        return [

        ]

    def execute(self):
        pass

    @classmethod
    def log(cls, *s, tp: str = ""):
        cls.logs.append(f'{" ".join(str(s1) for s1 in s)}')

    @classmethod
    def draw(cls, s, tp: str):
        from common.third_util.draw import Draw
        d = Draw()
        if tp.startswith('bar'):
            d.draw_bar_chart(s)
        elif tp.startswith('graph'):
            d.draw_graph(s)
        d.save(f"data/log/{tp}.png")

    def run(self):

        for i, case in enumerate(self.get_cases()):
            self.__class__.logs = []
            if isinstance(case, str):
                case = SolutionBase.case_load(
                    [v for v in case.split('\n') if v])
            self.ep = case.pop("result")
            a = time.time()
            try:
                self.init(**case)
                r = self.execute()
                self.log("finish", time.time()-a)
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, self.ep):
                self.flush_log(
                    i, f'case: {case}; result: {r}; except: {self.ep}')
            else:
                self.flush_log(i, "")

    def flush_log(self, i, s):

        fp = File(f'data/log/solution/{self.name}/{i}.log')
        if s:
            fp.write_file("\n".join([s]+self.__class__.logs))
        else:
            fp.write_file("")

    @classmethod
    def cls_run(cls):
        for case in cls.get_cases():
            cls.logs = ""
            m, inp, es = case
            r = cls(*inp[0])
            cls.log(m[0], *inp[0])
            for i in range(1, len(inp)):
                cls.log(m[i], inp[i], es[i])
                try:
                    e = getattr(r, m[i])(*inp[i])
                except Exception as a:
                    e = a
                if not r.diff(e, es[i]):
                    cls.log(f'result:{e}, expect:{es[i]}')
                    cls.flush_log(i)

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return str(a) == str(b)

    def init(self):
        pass

    def record(self):
        childs = []
        key = ""
        for k in self.watch_var:
            var=getattr(self,k)
            childs.append(to_json(var))
            key += hex_str(var)
        return key, childs


def hex_str(v):
    if hasattr(v, 'hex_str'):
        return v.hex_str()
    return str(v)


def to_json(v):
    if hasattr(v, 'to_json'):
        return v.to_json()
    return dict(title=str(v))


def ui_info(v):
    if hasattr(v, 'ui_info'):
        return v.ui_info()
    return dict(type='text')


PATH = 'app/yly/leetcode/view'


class Route:

    def query(self, path=PATH):
        ret = Node(value=path)
        for name in os.listdir(path):
            if not name.endswith('.py'):
                continue
            moudle_name = path.replace('/', '.')+"."+name.replace('.py', '')
            f: SolutionBase = Module().load_module(moudle_name, fun_name='Solution')()
            ret.add_child(value=moudle_name, data=f.get_cases())
        return ret

    def execute(self, moudle_name="app.yly.leetcode.view.3165", case: dict = None):
        f: SolutionBase = Module().load_module(moudle_name, fun_name='Solution')()
        if case is None:
            case = f.get_cases()[0]
        ans = case.pop("result")
        f.init(**case)
        return dict(option=dict(
            nodes=[ui_info(getattr(f,k)) for k in f.watch_var],
            records=run_watch_fun(f.execute, f.record)
        ))


if __name__ == "__main__":
    # print(http_test('/app/yly/manage/'+sys.argv[1]))
    json.dump(Route().execute(), open("data/a.json", 'w'), indent=4)
