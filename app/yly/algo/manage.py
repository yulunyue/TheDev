from common.tool.thread_util import run_watch_fun
from common.service.http import Node, http_test
from typing import List
from common.util.module import Module
from common.util.model import NumberModel,number
from common.util.log import logger
from common.util.fp import File
from collections import defaultdict
import os
import time
import sys
import json
CHANGE_STORE = dict()


def wc(title, key, v, color,sp):
    k = f'{title}{key}'
    size=""
    v = str(v)
    tp='span'
    # font-size:28px
    if v != CHANGE_STORE.get(k, v):
        CHANGE_STORE[k] = v
        size=f'color:{color}'
        tp = 'b'
    CHANGE_STORE[k] = v
    return f'<{sp}><span>{title}:</span><{tp} style="margin-left:4px;{size}">{v}</{tp}></{sp}>'



class WatchAny(Node):
    def __init__(self, *args, hex_str=None, algo_view=None,size=None,**kwargs) -> None:
        self.hex_str = hex_str
        self._algo_view = algo_view
        self.leaf:List[WatchAny]=[]
        if size is None:
            size=1 if algo_view else 0
        super().__init__(**kwargs,childs=args,size=size)
    
    def algo_view(self):
        ret=self._algo_view() if self._algo_view else ""
        if isinstance(ret,list):
            ret="</br></br>".join(ret)
        if isinstance(ret,str):
            ret=dict(title=ret)
        return ret

    
    def load(self):
        self.leaf =[]
        def dfs(c:WatchAny):
            for n in c.childs:
                dfs(n)
            if c._algo_view is not None:
                self.leaf.append(c)
        dfs(self)
        return self




def ah(txt, href):
    return f'<a href="{href}">{txt}</a>'


def bp(title, value, key=""):
    return wc(title, key, value, 'blue','p')

def bs(title, value, key=""):
    return wc(title, key, value, 'blue','span')



def div(*args,hex_str=None, algo_view=None,size=None,**kg):
    return WatchAny(*args,type='div', hex_str=hex_str, algo_view=algo_view, size=size,**kg)

HORIZONTAL = 0
VERTICAL = 1
def divh(*args,hex_str=None, algo_view=None,size=None):
    return div(*args,hex_str=hex_str, algo_view=algo_view,size=size,direction=HORIZONTAL)

def divv(*args, hex_str=None, algo_view=None,size=None):
    return div(*args,hex_str=hex_str, algo_view=algo_view,size=size,direction=VERTICAL)

def tree(t:WatchAny,size=None):
    return WatchAny(type='tree',hex_str=t.hex_str,algo_view=t.algo_view,size=size)

def grid(algo_view,hex_str=None):
    return WatchAny(type='grid',algo_view=algo_view,hex_str=hex_str)


    

    

class Util:
    def __init__(self) -> None:
        self.op=defaultdict(lambda:defaultdict(str))

    # def get_node(self,k)->Node:
        
    #     if k not in self.op:
    #         self.op[k]=Node(key=v,title=info)
    #     return self.op[v]
    def fmax(self,a,b,n,f,info):
        # a,b=number(a),number(b)
        if a<b:
            self.op[b][f]=info
            return b
        return a

    def fmin(self,a,b,n,f,info):
        # a,b=number(a),number(b)
        if a>b:
            self.op[b][f]=info
            return b
        return a

    def get_info(self,n,b):
        ret=[f'{b}']
        while b in self.op:
            a=self.op[b]
            b,info=list(a.items())[0]
            ret.append(f'{info} {b}')
        return "\n".join(ret)



U=Util()
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

    def execute(self,**kg):
        return self.exec(**kg)

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
        exec_names=['execute']+sys.argv[1:]
        for exec_name in exec_names:
            for i, case in enumerate(self.get_cases()):
                self.__class__.logs = []
                self.ep = case.pop("result")
                a = time.time()
                try:
                    self.log(f"begin {self.name}-{exec_name}")
                    self.pre(**case)
                    self.init(**case)
                    r = getattr(self,exec_name)(**case)
                    self.log(f"finish {self.name}-{exec_name}", time.time()-a)
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
        flag=False

        for var in self.watch_var.leaf:
            if var.hex_str is None:
                childs[var.key]=var.algo_view()
                continue
            key2,s2=var.key+'_algo',var.hex_str()
            childs[var.key]=var.algo_view()
            if CHANGE_STORE.get(key2)!=s2:
                flag=True
            CHANGE_STORE[key2]=s2
        if flag:
            return childs
        

    
    def info_main(self):
        return [
            f'{self.name}',
            f'{ah("链接",self.uri)}',
            f"标签: {self.tags}",
        ]
    
    def left(self):
        return []
    
    def left_c(self):
        return div(
            divh(
                algo_view=self.info_main,
            ),
            *self.left()
        )
    
    def get_watch(self):
        a=self.top()
        b=self.main()
        if a:
            return div(a,b)
        return b
    
    def top(self):
        pass
    
    def main(self):
        raise Exception("todo")


    def watch(self):
        self.watch_var=divv(
            self.left_c(),
            self.get_watch()
        ).load()
        return self.watch_var.to_json()

PATH = 'app/yly/algo'
TMP_PATH = 'data/algo/main.py'
def get_md(moudle_name):
    try:
        return Module().load_module(moudle_name,fun_name='Solution')()
    except Exception as e:
        logger.error(e)
    
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
            if fc is None or not getattr(fc,'has_view',None):
                continue
            ret.add_child(
                key=module_name, 
                title=title,
                value=fp.read_file(),
                data=dict(
                    cases=fc.get_cases()
                )
            )
        return ret.to_json()

    def execute(self, content, case):
        if isinstance(case,str):
            case=json.loads(case)
        fp=File(TMP_PATH).write_file(content)
        module_name=fp.py_module_path()
        f: SolutionBase = get_md(module_name)
        CHANGE_STORE.clear()
        f.pre(**case)
        f.init(**case)
        ret=f.watch()
        ret["data"]['records'],msg=run_watch_fun(f.execute, f.record)
        if msg:
            raise Exception(msg)
        return ret
    
class Util:
    def test(self):
        fp=File('app/yly/algo/geometry/lc_3235.py')
        f: SolutionBase = get_md(fp.py_module_path())
        File('data/algo/test.json').write_file(Route().execute(fp.read_file(),f.get_cases()[0]))
        
if __name__ == "__main__":
    Util().test()
