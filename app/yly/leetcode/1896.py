from typing import List,Dict,Optional
from collections import defaultdict, deque,Counter
from itertools import accumulate,product
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf=float("inf")
null=None
true=True
false=False
M=10**9 + 7


class Solution:
    def get_cases(self):
        return [
            dict(expression ="(((0)&1&((0&0))))",result=2),
            dict(expression = "0|((0|(0&0)))",result=0),
            dict(expression = "1&(0|1)",result=1),
            dict(expression = "(0|(1|0&1))",result=1),
            dict(expression = "(0&0)&(0&0&0)",result=3),
            
        ]
    def minOperationsToFlip(self, expression: str) -> int:
        op_fn={
            '&':lambda a,b:a&b,
            '|':lambda a,b:a|b
        }
        def util(s:str):
            stacks:List[list]=[]
            ans,state,last_op2=[None,None],None,None
            def set_state(state1,last_op,ans1):
                if last_op is None:
                    return ans1,state1
                else:
                    if last_op=='&':
                        ans2=min(ans[0],ans1[0]),min(ans[1]+ans1[1],ans[1]+1,ans1[1]+1)
                    else:
                        ans2=min(ans[0]+ans1[0],ans[0]+1,ans1[0]+1),min(ans[1],ans1[1])
                    self.log(state,ans,last_op,state1,ans1,ans2,stacks)
                    return ans2,op_fn[last_op](state)
                
            for si in s:
                if si=='(':
                    stacks.append([])
                elif si==')':
                    s3="".join(stacks.pop())
                    ans1,state1=util(s3)
                    ans,state=set_state(state1,last_op2,ans1)
                    if stacks:
                        stacks[-1].append(str(state))    
                elif stacks:
                    stacks[-1].append(si)    
                elif si not in op_fn:
                    state1=1 if si=='1' else 0
                    ans1=[1,0] if si=='1' else [0,1]
                    ans,state=set_state(state1,last_op2,ans1)
                else:
                    last_op2=si

            self.log(f'ep:[{s}]',ans,state)
            return ans,state
        ret,s=util(expression)
        return ret[1-s]
    def test(self,**kg):
        return self.minOperationsToFlip(**kg)


    def __init__(self,*args) -> None:
        self.local_debug=getattr(self,sys.argv[-1],None)
        if self.local_debug is None:
            print(sys.argv[-1],"not find")
    logs = ""
    def log(self, *s,tp:str=""):
        if not self.local_debug or len(self.logs)>=2048:
            return
        if tp:
            self.draw(s[0],tp)
        self.logs += " ".join([str(v) for v in s])+"\n"
    def draw(self,s,tp:str):
        from common.tool.draw import Draw
        d=Draw()
        if tp.startswith('bar'):
            d.draw_bar_chart(s)
        elif tp.startswith('graph'):
            d.draw_graph(s)
        d.save(f"data/log/{tp}.png")
    
    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs=""
            ep=case.pop("result")
            try:
                r=self.local_debug(**case)
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r=None
            if not self.diff(r,ep):
                print(case,r,ep)
                print(self.logs)
                break
            
    def diff(self,a,b):
        if isinstance(a,float) and isinstance(b,float):
            return "%.2f"%(a)=="%.2f"%(b)
        return a==b

    



      

if __name__ == '__main__':
    Solution().run()



