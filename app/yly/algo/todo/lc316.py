from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(s="abacb",result='abc'),
            dict(s="bcabc",result='abc'),
            dict(s = "cbacdcbc",result="acdb")
        ]
    def execute(self, s: str) -> str:
        r=defaultdict(int)
        vt=set()
        ans=[]
        for v in s:
            r[v]+=1
        for v in s:
            r[v]-=1
            if v in vt:
                continue
            while ans and v<=ans[-1] and r[ans[-1]]:
                vt.remove(ans.pop())
            ans.append(v)
            vt.add(v)
        return "".join(ans)

    def removeDuplicateLetters(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)



if __name__=='__main__':
    Solution().run()