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
    if v != CHANGE_STORE.get(key, v):
        CHANGE_STORE[key] = v
        return f'<span style="color:blue">{v}</span>'
    CHANGE_STORE[key] = v
    return v


class WatchVar:
    def __init__(self) -> None:
        self.watch_ins = None
        self.watch_keys = None
        self._ins = None

    def set_json_view(self, watch_ins, _type="text", _ins=None, **watch_keys):
        self._ins = _ins
        self._type = _type
        self.watch_ins = watch_ins
        self.watch_keys = watch_keys
        return self

    def hex_str(self):
        if self._type == 'text':
            return "".join(str(getattr(self.watch_ins, key)) for key in self.watch_keys.keys())
        return self._ins.hex_str()

    def to_json(self):

        if self._type == 'text':
            childs = []
            for k, name in self.watch_keys.items():
                value = wc("self_"+k, str(getattr(self.watch_ins, k)))
                childs.append(dict(title=name+":", value=value))
            return dict(childs=childs)
        return self._ins.to_json()

    def ui_info(self):
        return dict(type=self._type)


class SolutionBase:
    logs = []
    case_load = None
    name = "test"
    DEV = True
    watch_var = None

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
        return WatchVar().set_json_view(self, **kw)

    def record(self):
        childs = []
        key = ""
        for var in self.watch_var:
            childs.append(var.to_json())
            key += var.hex_str()
        return key, childs

    def get_watch(self):
        return []


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

    def execute(self, moudle_name="app.yly.algo.seg_tree.3165", case: dict = None):
        f: SolutionBase = Module().load_module(moudle_name, fun_name='Solution')()
        if case is None:
            case = f.get_cases()[0]
        CHANGE_STORE.clear()
        f.init(**case)
        f.watch_var = f.get_watch()
        return dict(data=dict(
            nodes=[v.ui_info() for v in f.watch_var],
            records=run_watch_fun(f.execute, f.record)
        ))


if __name__ == "__main__":
    # print(http_test('/app/yly/manage/'+sys.argv[1]))
    open("data/a.json", 'w', encoding='utf-8').write(
        json.dumps(Route().execute('app.yly.algo.geometry.lc_3235'), indent=4,
                   ensure_ascii=False))
