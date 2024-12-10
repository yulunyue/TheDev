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

    def graph(self):
        return self.set_type("graph")
    
    def hex_str(self):
        node=getattr(self.ins,self.key,None)
        return str(node)
    
    def set_ins(self,ins):
        self.ins=ins
        return self
    
    def view(self):
        node=getattr(self.ins,self.key)
        if self.type == 'tree':
            return node.tree_view()
        if self.type == 'graph':
            return node.graph_view()
        return dict(data=bp(self.key,str(node),'self'),type=self.type)
    
    def to_json(self):
        return super().to_json(size=self.size)


class SolutionBase:
    _logs = []
    _has_view = False
    _name = ""
    _DEV = True
    _gameinfo = ['lc']
    _tags = []
    _watch_var:List[View] = None
    action="log"
    def get_cases(self):
        return [

        ]

    def execute(self):
        return self.exec()


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
    
    def pre(self,input=None,result=None,**kwargs):
        if input is not None:
            self.lines=[v for v in input.split('\n') if v]
    
    def gen_file(self):
        write_path='data/algo/run.py'
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
                    lines.extend(data)
                else:
                    lines.append(ln)
            else:
                lines.append(ln)
        File(write_path).write_file("\n".join(lines))
    
    def run(self):
        exec_names=sys.argv[1:]
        if exec_names and exec_names[0]=='view_md':
            return self.view_md()
        if exec_names and exec_names[0]=='view_web':
            return self.view_web()
        if not exec_names:
            exec_names = ['execute']
            self.gen_file()
        for exec_name in exec_names:
            for i, case in enumerate(self.get_cases()):
                self.__class__._logs = []
                self.ep = case.pop("result")
                a = time.time()
                try:
                    self.log(f"begin {self._name}-{exec_name}")
                    self.pre(**case)
                    self.init(**case)
                    r = getattr(self,exec_name)()
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
                CHANGE_STORE[key2]=s2
            childs[var.key]=var.view()
            
        if flag:
            return childs
    
    def get_watch(self):
        return []
    def get_main_view(self):
        return View().add_node(*self.get_watch())
    def init_watch(self,tp):
        if self._watch_var is not None:
            return
        node:View=self.get_main_view()
        keys=[]
        self._watch_var = []
        def dfs(p:View):
            if not p.childs:
                self._watch_var.append(p.set_ins(self))
            for c in p.childs:
                dfs(c)
        dfs(node)



    def view_md(self):
        case,ret,msg = self.view(tp="md")
        ReadmeGen(
            f'data/algo/{self.get_name()}/readme'
        ).add_table(
            case
        ).set_frames(ret).save()

    def view_web(self):
        _,ret,_ = self.view()
        File(f'data/algo/{self.get_name()}/readme.json').write_file(ret)

    def view(self,case=None,tp='web'):
        if case is None:
            case=self.get_cases()[0]
        CHANGE_STORE.clear()
        self.pre(**case)
        self.init(**case)
        self.init_watch(tp)
        ret1,msg=run_watch_fun(self.execute, self.record)
        ret=self.get_main_view().to_json()
        ret['data']=dict(record=ret1)
        if msg:
            raise Exception(msg)
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
    
        

