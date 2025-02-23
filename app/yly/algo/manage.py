from common.tool.thread_util import run_watch_fun
from common.service.http import Node, http_test
from typing import List,Dict,Optional
import bisect
from common.util.module import Module
from common.util.log import logger
from common.util.fp import File
from collections import defaultdict
import functools
from common.third_util.cg_util import CodingGame
import heapq
import os
import time
import math
import sys
import json
import numpy as np
sys.setrecursionlimit(10**5+1)
import bisect
MOD=(10**9)+7
inf = float("inf")
WRITE_PATH='data/algo/run.py'
CHANGE_STORE = dict()
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left:TreeNode = None
        self.right:TreeNode = None

    @staticmethod
    def load_from_lc_array(array):
        ret = [None]+[TreeNode(v) for v in array]
        for v in range(2,len(ret)):
            if ret[v].val is None:
                continue
            if v%2==0:
                ret[v//2].left=ret[v]
            else:
                ret[v//2].right=ret[v]
        return ret[1]

def color(a,b):
    return '#ccc' if a==b else '#fff'

def bp(title, value, key=""):
    return wc(title, key, value, 'blue')


def wc(title, key, v, change_color,sp='p'):
    v = str(v)
    k=f'{title}_{key}'
    # font-size:28px
    color=""
    if k in CHANGE_STORE and v!=CHANGE_STORE[k]:
        color=change_color
    CHANGE_STORE[k] = v
    return dict(
        key=k,
        title=title,
        value=v,
        color=color,
        type='p'
    )



class View(Node):
    def __init__(self, key="",size=1,**kwargs) -> None:
        type = 'pre' if key else 'div'
        super().__init__(type=type,key=key,size=size,**kwargs)
    
    def tree(self):
        return self.set_type("tree")

    def grid(self):
        return self.set_type("grid")
    
    def graph(self):
        return self.set_type("graph")
    
    def list(self):
        return self.set_type("list")
    
    def hex_str(self):
        node=getattr(self.ins,self.key,None)
        return str(node)
    
    def set_ins(self,ins):
        self.ins=ins
        return self
    
    def view(self):
        node=getattr(self.ins,self.key)
        if self.type == 'list':
            return dict(data=node, type=self.type)
        if hasattr(node,f'{self.type}_view'):
            return getattr(node,f'{self.type}_view')()
        return dict(data=bp(self.key,str(node),'self'),type=self.type)
    
    def to_json(self):
        return super().to_json(size=self.size)

def fmax(a,b,*args):return a if a>b else b
def fmin(a,b,*args):return a if a<b else b
class SolutionBase:
    uri=""
    log_mode='test'
    _logs = []
    _has_view = False
    name = "solution"
    _DEV = True
    _tags = []
    _watch_var:List[View] = None
    log_str="log"
    game_id=""
    results = []
    def get_cases(self):
        return [

        ]
    
    def execute(self,*args,**kw):
        self.exec()
        return "\n".join(self.results)

    def log(self, s, tp: str = ""):
        s=str(s)
        if isinstance(tp,str):
            if tp:
                raise Exception(tp)
        else:
            fs=s.split(',')
            s="; ".join([f'{k}:{tp.get(k) if isinstance(tp,dict) else getattr(tp,k)}' for k in fs])
        self.log_str = s
        if self.log_mode=='debug':
            logger.info(s)
        else:
            self._logs.append(self.log_str)
        
    def pre(self,input="",result=None,**kwargs):
        if 'codingame' in  self.uri:
            data=File(f"data/log/cg/{self.name}.json").read_file()
            kwargs['stderr']=[]
            kwargs['stdout']=[]
            for v in data['frames']:
                if 'stderr' in v:
                    kwargs['stderr'].append(json.loads(v['stderr']))
                if 'stdout' in v:
                    kwargs['stdout'].append(v['stdout'].split('\n')[0])
        self.lines=[v for v in input.split('\n') if v]
        return kwargs
    def gen_file(self):
        lines=[]
        def read_file(md_name:str):
            path=""
            if md_name=='app.yly.algo.manage':
                path='app/yly/algo/base.py'
            elif md_name.startswith('common.algo'):
                path=sys.modules[md_name].__file__
            if path:
                return File(path).read_line()
        for ln in File(sys.argv[0]).read_line():
            if not ln:continue
            elif ln.startswith('from'):
                data=read_file(ln.split(' ')[1])
                if data:
                    lines.extend([d for d in data if not d.startswith('from common')])
                else:
                    lines.append(ln)
            else:
                lines.append(ln)
        File(WRITE_PATH).write_file("\n".join(lines))
    
    def exec(self):
        pass
    
    def run(self):
        exec_names=sys.argv[1:]
        self.gen_file()
        if exec_names and exec_names[0]=='view_web':
            return self.view_web()
        if exec_names and exec_names[0]=='submit':
            return self.submit()

        self.test([getattr(self,v) for v in exec_names[0].split(',')])
        self.flush_log()

    agentsIds=None
    def submit(self):
        if 'codingame' in  self.uri:
            ret=CodingGame(self.name).pk(
                WRITE_PATH,self.game_id,self.agentsIds
            )
            File(f"data/log/cg/{self.name}.json").write_file(ret)
        else:
            raise Exception(self.uri)

    def test(self, func):
        if self.uri.startswith('lc_cls'):
            return self.run_cls()
        for fn in func:
            for i, case in enumerate(self.get_cases()):
                self.ep = case.get("result")
                self.results=[]
                a = time.time()
                self.log(f"begin {self.name}-{fn.__name__}")
                self.log(f'case: {case}; except: {self.ep}')
                case=self.pre(**case)
                self.init(**case)
                r = fn(**case)
                if r is None:
                    r="\n".join(self.results)
                self.log(f"finish {self.name}-{fn.__name__}; result: {r}; use_time: {time.time()-a}")
                if self.ep is not None and not self.diff(r, self.ep):
                    self.flush_log()
                    break
                if self.ep is not None:
                    self._logs=[]
        self.flush_log()
                
                
            
    def error(self,*args):
        pass
    
    def output(self,s):
        self.results.append(str(s))

    def input(self)->str:
        while self.lines and not self.lines[0]:
            self.lines.pop(0)
        if self.lines:
            return self.lines.pop(0)
    
    def i1(self):
        s=self.input()
        if s is None:
            return
        return int(s)
    
    def il(self):
        return [int(v) for v in self.input().split(' ') if v]
    
    def flush_log(self):
        if self._logs:
            logger.info("\n"+"\n".join(self._logs))
            self._logs.clear()



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
                # logger.info(f'{key2}:{CHANGE_STORE.get(key2)},{s2}')
                CHANGE_STORE[key2]=s2
            childs[var.key]=var.view()
        if flag:
            return childs
    
    def get_watch(self):
        return []
    def get_main_view(self):
        return View().add_node(*self.get_watch())
    
    def init_watch(self):
        if self._watch_var is not None:
            return
        node:View=self.get_main_view()
        self._watch_var = []
        def dfs(p:View):
            if not p.childs:
                self._watch_var.append(p.set_ins(self))
            for c in p.childs:
                dfs(c)
        dfs(node)

    def view_web(self):
        _,ret,_ = self.view()
        path=f'data/algo/{self.name}/record.json'
        File(path).write_file(ret)
        logger.info(path)

    def view(self,case=None):
        if case is None:
            case=self.get_cases()[0]
        CHANGE_STORE.clear()
        self.pre(**case)
        self.init(**case)
        self.init_watch()
        ret1,msg=run_watch_fun(self.execute, self.record)
        ret=self.get_main_view().to_json()
        ret['data']=dict(record=ret1)
        if msg:
            raise Exception(msg)
        return case,ret,msg  

    def run_cls(self):
        self.gen_file()
        for case in self.get_cases():
            method,param,result=case['mathods'],case['params'],case['result']
            self.init()
            self._logs.clear()
            flag=False
            self.log(f'{method} {param} {result}')
            for i in range(1,len(method)):
                e=getattr(self,method[i])(*param[i])
                self.log(f'{i} {method[i]} {param[i]} {e}')
                if e!=result[i]:
                    self.log(f'ans:{result[i]}')
                    flag=True
                    break
            if flag:
                break
            self._logs.clear()
        self.flush_log()



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
            if fc is None or not getattr(fc,'_has_view',None):
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
        _,ret,msg=f.view(case)
        # if msg:
        #     raise Exception(msg)
        return ret
    
        

