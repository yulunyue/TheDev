from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf
class Solution(SolutionBase):
    def get_cases(self):
        return [

        ]
    
    def compareVersion(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
    def execute(self,version1:str,version2:str,**kw):
        v1=[int(v) for v in version1.split('.')]
        v2=[int(v) for v in version2.split('.')]
        if len(v1)<len(v2):
            v1+=[0]*(len(v2)-len(v1))
        else:
            v2+=[0]*(len(v1)-len(v2))
        for i in range(len(v1)):
            if v1[i]<v2[i]:
                return -1
            if v1[i]>v2[i]:
                return 1
        return 0



if __name__=='__main__':
    Solution().run()