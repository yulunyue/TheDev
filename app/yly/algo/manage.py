from common.tool.thread_util import run_watch_fun
from common.service.http import Node, http_test
from typing import List
from common.util.module import Module
from common.util.model import NumberModel,number
from common.util.log import logger
from common.util.fp import File
from collections import defaultdict
from common.tool.readme import ReadmeGen
import os
import time
import sys
import json
CHANGE_STORE = dict()
def ah(txt, href):
    return f'<a href="{href}">{txt}</a>'


def bp(title, value, key=""):
    return wc(title, key, value, 'blue','p')

def bs(title, value, key=""):
    return wc(title, key, value, 'blue','span')

def wc(title, key, v, color,sp='p'):
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
    def get_title(self):
        return str(getattr(self.ins,self.key))
    
    def hex_str(self):
        return self.get_title()
    
    def set_ins(self,ins):
        self.ins=ins
        return self


class SolutionBase:
    _logs = []
    _has_view = False
    _name = ""
    _DEV = True
    _gameinfo = ['lc']
    _tags = []
    _watch_var:List[WatchAny] = None
    action=""
    def get_cases(self):
        return [

        ]

    def execute(self,**kg):
        return self.exec(**kg)


    def log(self, *s, tp: str = ""):
        self.action = f'{" ".join(str(s1) for s1 in s)}'
        self._logs.append(self.action)

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
        exec_names=sys.argv[1:]
        if exec_names and exec_names[0]=='view_md':
            return self.view_md()
        if exec_names and exec_names[0]=='view_font':
            return self.view_font()
        if not exec_names:
            exec_names = ['execute']
        for exec_name in exec_names:
            for i, case in enumerate(self.get_cases()):
                self.__class__._logs = []
                self.ep = case.pop("result")
                a = time.time()
                try:
                    self.log(f"begin {self._name}-{exec_name}")
                    self.pre(**case)
                    self.init(**case)
                    r = getattr(self,exec_name)(**case)
                    self.log(f"finish {self._name}-{exec_name}", time.time()-a)
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    r = None
                if not self.diff(r, self.ep):
                    logs = "\n".join(self.__class__._logs)
                    self.flush_log(
                        i, f'case: {case}; result: {r}; except: {self.ep}\n{logs}')
                    break
    def input(self)->str:
        while self.lines and not self.lines[0]:
            self.lines.pop(0)
        return self.lines.pop(0)
    
    def i1(self):
        return int(self.input().strip())
    
    def il(self):
        return [int(v) for v in self.input().split(' ') if v]
    
    def flush_log(self, i, s):
        logger.info(f'{i}:{s}')

    @classmethod
    def cls_run(cls):
        for case in cls.get_cases():
            cls._logs = []
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

        for var in self._watch_var:
            key2,s2=var.key+'_algo',var.hex_str() if var.hex_str else ""
            if CHANGE_STORE.get(key2)!=s2:
                flag=True
                childs[var.key]=var.to_json()
                CHANGE_STORE[key2]=s2
            
        if flag:
            return childs
        
    
    def init_watch(self,tp):
        if self._watch_var is not None:
            return
        self._watch_var=[]
        for key in dir(self):
            if key.startswith('_'):
                continue
            v=getattr(self,key)
            if isinstance(v,(str,dict,int,float,list)):
                self._watch_var.append(WatchAny(key=key).set_ins(self))
            elif isinstance(v,WatchAny):
                v.key=key
                self._watch_var.append(v)

    def view_md(self):
        case,ret,msg = self.view(tp="md")
        ReadmeGen(
            f'data/algo/{self.get_name()}/readme'
        ).add_table(
            case
        ).set_frames(ret).save()

    def view_font(self):
        _,ret,_ = self.view()
        File(f'data/algo/{self.get_name()}/readme.json').write_file(ret)

    def view(self,case=None,tp='font'):
        if case is None:
            case=self.get_cases()[0]
        CHANGE_STORE.clear()
        self.pre(**case)
        self.init(**case)
        self.init_watch(tp)
        ret,msg=run_watch_fun(self.execute, self.record)
        return case,ret,msg  
    def get_name(self):
        return self._name or self.__class__.__name__

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
        ret,msg=f.view(case)
        if msg:
            raise Exception(msg)
        return ret
    
        

