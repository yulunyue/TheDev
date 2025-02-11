from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(num1=1,dec=2,result="0.5"),
            dict(num1=80,dec=3,result="26.(6)"),
            dict(num1=8,dec=300,result="0.02(6)"),
            dict(num1=5,dec=7,result="0.(714285)")
        ]
    
    def fractionToDecimal(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
    def execute(self,num1,dec,**kw):
        ct=dict()
        z,num1=num1//dec,num1%dec        
        s=[f'{z}.']
        while num1*10<dec:
            num1*=10
            s.append('0')
        # zero_num=0
        while num1:
            num1*=10
            d,num1=num1//dec,num1%dec
            if d in ct:
                s.insert(ct[d],'(')
                s.append(')')
                break
            ct[d]=len(s)
            s.append(str(d))
           
    
        return "".join(s)


if __name__=='__main__':
    Solution().run()