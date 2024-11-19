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
    cl = '#000'
    if v != CHANGE_STORE.get(k, v):
        CHANGE_STORE[key] = v
        cl = color
    CHANGE_STORE[key] = v
    return f'<span>{title}</span><span style="color:{cl};margin:3px">{v}</span>'


def li(array, method_name):
    if isinstance(array, list):
        return [li(v, method_name) for v in array]
    return getattr(array, method_name)()


def rs(title, value, key=""):
    return wc(title, key, value, 'red')


def ah(txt, href):
    return f'<a href="{href}">{txt}</a>'


def bs(title, value, key=""):
    return wc(title, key, value, 'blue')


def gs(title, value, key):
    return wc(title, key, value, 'green')


class WatchAny:
    def __init__(self, tp, *args, hex_str=None, algo_view=None, size=0) -> None:
        self.hex_str = hex_str
        self.algo_view = algo_view
        self.type = tp
        self.size = size
        self.childs:List[WatchAny] = list(args)
        self.leaf:List[WatchAny]=[]
    def ui_info(self):
        return dict(
            type=self.type, 
            size=self.size,
            childs=[v.ui_info() for v in self.childs]
        )

    def set_type(self, v):
        self.type = v
        return self
   
    def load(self):
        self.leaf =[]
        def dfs(c:WatchAny):
            for n in c.childs:
                dfs(n)
            if not c.childs:
                if c.algo_view is None or c.hex_str is None:
                    raise Exception(c,c.type,c.childs)
                self.leaf.append(c)
        dfs(self)
        return self


class SolutionBase:
    logs = []
    has_view = False
    name = "test"
    DEV = True
    gameinfo = ['lc']
    watch_var:WatchAny
    
    def get_cases(self):
        return [

        ]

    def execute(self):
        pass

    def algo_view(self):
        return []

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

    def exec(self,**kg):
        pass

    def run(self):
        for i, case in enumerate(self.get_cases()):
            self.__class__.logs = []
            self.ep = case.pop("result")
            a = time.time()
            try:
                self.init(**case)
                if self.gameinfo[0]=='cf':
                    self.lines=[v for v in case.pop('input').split('\n') if v]
                    r = self.exec(**case)
                else:
                    r = self.execute(**case)
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
    def input(self):
        return self.lines.pop(0)

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
    
    def layout(self,tp,*args, hex_str=None, algo_view=None, size=0,**kw):
        return WatchAny(tp, *args, hex_str=hex_str, algo_view=algo_view, size=size,**kw)
    
    def record(self):
        childs = []
        keys = []
   
        for var in self.watch_var.leaf:
            childs.append(var.algo_view())
            keys.append(var.hex_str())
        # dfs(self.watch_var)
        return "".join(keys), childs

    def get_watch(self):
        raise Exception("xx")


PATH = 'app/yly/algo'


class Route:

    def query(self, **kwargs):
        ret = Node(value=PATH)

        for fp in File(PATH).dp_dir():
            if not fp.path.endswith('.py'):
                continue
            moudle_name = fp.path.replace('/', '.').replace('.py', '')
            fc = Module().load_module(moudle_name)
            if hasattr(fc, 'has_view') and getattr(fc, 'has_view'):
                ret.add_child(value=moudle_name, data=fc.get_cases())
        return ret

    def execute(self, moudle_name, case: dict = None):
        f: SolutionBase = Module().load_module(moudle_name, fun_name='Solution')()
        if case is None:
            case = f.get_cases()[0]
        CHANGE_STORE.clear()
        f.init(**case)
        f.watch_var = f.get_watch()
        ret=f.watch_var.ui_info()
        ret["data"]=dict(records=run_watch_fun(f.execute, f.record))
        return ret

if __name__ == "__main__":
    # print(http_test('/app/yly/manage/'+sys.argv[1]))
    open("data/a.json", 'w', encoding='utf-8').write(
        json.dumps(Route().execute('app.yly.algo.seg_tree.lc_3165'), indent=4,
                   ensure_ascii=False))
    # print(Route().query().to_json())
