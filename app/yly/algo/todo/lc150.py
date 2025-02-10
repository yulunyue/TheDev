from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(tokens=["2","1","+","3","*"],result=9)
        ]
    
    def evalRPN(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
    def execute(self,tokens:List[str],**kw):
        op={
            "+":lambda a,b:a+b,
            "-":lambda a,b:a-b,
            "*":lambda a,b:a*b,
            "/":lambda a,b:a/b
        }
        i=0
        while len(tokens)>1:
            if tokens[i] in op:
                i=i-2
                a=int(tokens.pop(i))
                b=int(tokens.pop(i))
                c=tokens.pop(i)
                tokens.insert(i,op[c](a,b))
            else:
                i+=1
        return tokens[0]



if __name__=='__main__':
    Solution().run()