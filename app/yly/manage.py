from common.tool.thread_util import run_watch_fun
from common.service.http import Node, http_test
from typing import List
from common.util.module import Module
from common.util.log import logger
from common.util.fp import File
import os
import time
import sys
import json
CHANGE_STORE = dict()


def wc(key, v):
    if v != CHANGE_STORE.get(key):
        CHANGE_STORE[key] = v
        return f'<span style="color:blue">{v}</span>'
    return v


class WatchVar:
    def __init__(self) -> None:
        self._type = "text"
        self.watch_ins = None
        self.watch_keys = None

    def set_json_view(self, watch_ins, watch_keys):
        self.watch_ins = watch_ins
        self.watch_keys = watch_keys
        return self

    def hex_str(self):
        if isinstance(self.watch_keys, dict):
            return "".join(str(getattr(self.watch_ins, key)) for key in self.watch_keys.keys())
        return ""

    def to_json(self):
        value = ""
        if isinstance(self.watch_keys, dict):
            value = "</br>".join([f'{name}: {wc("self_"+k,getattr(self.watch_ins, k))}' for k,
                                 name in self.watch_keys.items()])
        return dict(title=value)

    def ui_info(self):
        return dict(type=self._type)


class SolutionBase:
    logs = []
    case_load = None
    name = "test"

    def __init__(self) -> None:
        self.watch_var: List[WatchVar] = []

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

    def init(self, *args, **kwargs):
        pass

    def watch(self, **kw):
        return WatchVar().set_json_view(self, kw)

    def record(self):
        childs = []
        key = ""
        for var in self.watch_var:
            childs.append(var.to_json())
            key += var.hex_str()
        return key, childs


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
        f.init(**case)
        return dict(data=dict(
            nodes=[v.ui_info() for v in f.watch_var],
            records=run_watch_fun(f.execute, f.record)
        ))


if __name__ == "__main__":
    # print(http_test('/app/yly/manage/'+sys.argv[1]))
    open("data/a.json", 'w', encoding='utf-8').write(
        json.dumps(Route().execute(), indent=4,
                   ensure_ascii=False))
