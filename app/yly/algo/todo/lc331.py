from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(preorder="9,3,4,#,#,1,#,#,2,#,6,#,#",result=true)
        ]
    

    def execute(self, preorder: str) -> bool:
        stacks=[]
        for v in preorder.split(','):
            while v=='#' and stacks and stacks[-1]=='#':
                stacks.pop()
                stacks.pop()
            stacks.append(v)
        self.log(stacks)
        return len(stacks)==1
    
    def isValidSerialization(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)



if __name__=='__main__':
    Solution().run()