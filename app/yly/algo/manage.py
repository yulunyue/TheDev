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


def wc(title, key, v, color):
    k = title+key
    cl='#000'
    if v != CHANGE_STORE.get(k, v):
        CHANGE_STORE[key] = v
        cl=color 
    CHANGE_STORE[key] = v
    return f'<span>{title}</span><span style="color:{cl};margin:3px">{v}</span>'


def rs(title,value,key=""):
    return wc(title,key,value,'red')

def ah(txt,href):
    return f'<a href="{href}"></a>'

def bs(title,value,key=""):
    return wc(title,key,value,'blue')


def gs(title,value,key):
    return wc(title,key,value,'green')




class WatchAny:
    def __init__(self, tp,ins,size=0) -> None:
        self.ins =ins
        self.type=tp
        self.size=size

    def hex_str(self):
        return self.ins.hex_str()

    def algo_view(self):
        return self.ins.algo_view()
    
    
    def ui_info(self):
        return dict(type=self.type,size=self.size)

    def set_type(self, v):
        self.type = v
        return self


class SolutionBase:
    logs = []
    case_load = None
    name = "test"
    DEV = True
    watch_var = None
    gameinfo = ['lc']
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

    def run_cf(self):
        pass


    def run_lc(self):
        game_type,*args=self.gameinfo
        for i, case in enumerate(self.get_cases()):
            self.__class__.logs = []
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
                logs = "\n".join(self.__class__.logs)
                self.flush_log(
                    i, f'case: {case}; result: {r}; except: {self.ep}\n{logs}')
                break
    def run(self):
        if self.gameinfo[0]=='lc':
            self.run_lc()
        elif self.gameinfo[0]=='cf':
            self.run_cf()
    def flush_log(self, i, s):
        logger.info(f'{i}:{s}')

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

    def watch(self,tp,ins,size=0):
        return WatchAny(tp,ins,size)

    def record(self):
        childs = []
        key = ""
        for var in self.watch_var:
            childs.append(var.algo_view())
            key += var.hex_str()
        return key, childs

    def get_watch(self):
        return []


PATH = 'app/yly/algo'


class Route:

    def query(self, **kwargs):
        ret = Node(value=PATH)
        
        for fp in File(PATH).dp_dir():
            if not fp.path.endswith('.py'):
                continue
            moudle_name = fp.path.replace('/', '.').replace('.py', '')
            fc = Module().load_module(moudle_name)
            if not hasattr(fc, 'Solution'):
                continue
            f: SolutionBase = fc.Solution()
            cases = f.get_cases()
            if not cases:
                continue
            if isinstance(cases[0],dict): 
                f.init(**cases[0])
            if f.get_watch():
                ret.add_child(value=moudle_name, data=cases)
        return ret

    def execute(self, moudle_name, case: dict = None):
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
    # open("data/a.json", 'w', encoding='utf-8').write(
    #     json.dumps(Route().execute('app.yly.algo.geometry.lc_3235'), indent=4,
    #                ensure_ascii=False))
    print(Route().query().to_json())
