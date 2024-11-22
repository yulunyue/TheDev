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
    k = f'{title}{key}'
    cl = '#000'
    v = str(v)
    # print(k,v,CHANGE_STORE.get(k))
    if v != CHANGE_STORE.get(k, v):
        CHANGE_STORE[k] = v
        cl = color
    
    CHANGE_STORE[k] = v
    return f'<span>{title}:</span><span style="color:{cl};margin:3px">{v}</span>'



class WatchAny(Node):
    def __init__(self, *args, hex_str=None, algo_view=None,size=None,**kwargs) -> None:
        self.hex_str = hex_str or algo_view
        self._algo_view = algo_view
        self.leaf:List[WatchAny]=[]
        if size is None:
            size=1 if algo_view else 0
        super().__init__(**kwargs,childs=args,size=size)
    
    def algo_view(self):
        ret=self._algo_view() if self._algo_view else ""
        if isinstance(ret,str):
            ret=dict(title=ret)
        return ret

    def get_hex_str(self):
        return self.hex_str()
        


   
    def load(self):
        self.leaf =[]
        def dfs(c:WatchAny):
            for n in c.childs:
                dfs(n)
            if c._algo_view is not None and c.hex_str is not None:
                self.leaf.append(c)
        dfs(self)
        return self

def rs(title, value, key=""):
    return wc(title, key, value, 'red')


def ah(txt, href):
    return f'<a href="{href}">{txt}</a>'


def bs(title, value, key=""):
    return wc(title, key, value, 'blue')


def gs(title, value, key):
    return wc(title, key, value, 'green')

def div(*args,hex_str=None, algo_view=None,size=None,**kg):
    return WatchAny(*args,type='div', hex_str=hex_str, algo_view=algo_view, size=size,**kg)
HORIZONTAL = 0
VERTICAL = 1
def divh(*args,hex_str=None, algo_view=None,size=None):
    return div(*args,hex_str=hex_str, algo_view=algo_view,size=size,direction=HORIZONTAL)

def divv(*args,hex_str=None, algo_view=None,size=None):
    return div(*args,hex_str=hex_str, algo_view=algo_view,size=size,direction=VERTICAL)

def tree(t:WatchAny,size=None):
    return WatchAny(type='tree',hex_str=t.hex_str,algo_view=t.algo_view,size=size)

class SolutionBase:
    logs = []
    has_view = False
    name = "test"
    DEV = True
    gameinfo = ['lc']
    tags = []
    watch_var:WatchAny
    
    def get_cases(self):
        return [

        ]

    def execute(self):
        return self.exec()

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
    
    def pre(self,input=None,**kwargs):
        if input is not None:
            self.lines=[v for v in input.split('\n') if v]

    def run(self):
        for i, case in enumerate(self.get_cases()):
            self.__class__.logs = []
            self.ep = case.pop("result")
            a = time.time()
            try:
                self.pre(**case)
                self.init(**case)
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
    def input(self)->str:
        return self.lines.pop(0)
    def i1(self):
        return int(self.input().strip())
    def il(self,n):
        return [[int(v) for v in self.input().split(' ')] for _ in range(n)]
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
    
    
    def record(self):
        childs = {}


        for var in self.watch_var.leaf:
            key2,s2=var.key+'_algo',var.get_hex_str()
            if CHANGE_STORE.get(key2)!=s2:
                childs[var.key]=var.algo_view()
            CHANGE_STORE[key2]=s2

        # dfs(self.watch_var)
        return childs

    def get_watch(self):
        raise Exception("xx")
    def hex_str(self):
        return ""
    def algo_view(self):
        return '<br><br>'.join([
            f'{self.name}',
            f'{ah("链接",self.uri)}',
            f"标签: {self.tags}",
        ]+self.get_info())
    
    def get_info(self):
        return []
    
    def watch(self):
        self.watch_var=divv(
            div(
                hex_str=self.hex_str,
                algo_view=self.algo_view,
                size=0,
            ),
            self.get_watch()
        ).load()
        return self.watch_var.to_json()

PATH = 'app/yly/algo'
TMP_PATH = 'data/algo/main.py'
def get_md(moudle_name):
    return Module().load_module(moudle_name,fun_name='Solution')()

Solution = SolutionBase
class Route:

    def query(self, **kwargs):
        ret = Node(value=PATH)
        for fp in File(PATH).dp_dir():
            if not fp.path.endswith('.py'):
                continue
            module_name = fp.py_module_path()
            title=module_name.split('.')[-1]
            fc:SolutionBase = get_md(module_name)
            if not fc.has_view:
                continue
            ret.add_child(
                value=module_name, 
                title=title,
                data=dict(
                    content=fp.read_file(),
                    cases=fc.get_cases()
                )
            )
        return ret.to_json()

    def execute(self, content, case):
        fp=File(TMP_PATH).write_file(content)
        module_name=fp.py_module_path()
        f: SolutionBase = get_md(module_name)
        CHANGE_STORE.clear()
        f.pre(**case)
        f.init(**case)
        ret=f.watch()
        ret["data"]['records']=run_watch_fun(f.execute, f.record)
        return ret
    
class Util:
    def test(self):
        fp=File('app/yly/algo/bcj/cf_195e.py')
        f: SolutionBase = get_md(fp.py_module_path())
        File('data/algo/test.json').write_file(Route().execute(fp.read_file(),f.get_cases()[0]))
        
if __name__ == "__main__":
    Util().test()
