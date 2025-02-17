from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,\
    Dict,List,MOD,inf,heapq
from common.algo.str_util import kmp_array,kmp_search
class Solution(SolutionBase):
    def get_cases(self):
        return [
            #dict(s="a"*(10**5),p="aa"*(10**2)+"*"+"bb"*(10**4)+"*"+"cc",result=0),
            dict(s = "madlogic", p = "*adlogi*",reuslt=6),
            dict(s="abc",p="a*b*c",result=3),
            dict(s='abaacbaecebce',p='"ba*c*ce',result=8),
            dict(s = "baccbaadbc", p = "cc*baa*adb",result=-1),
            dict( s = "a", p = "**",result=0),
        ]
    
    def shortestMatchingSubstring(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
    def execute(self,s,p:str):
        ps=[[len(v),kmp_search(s,v)] for v in p.split('*')]
        l=r=0
        ans=-inf
        self.log(ps)
        for v in ps[1][1]:
            while l<len(ps[0][1]) and ps[0][0]+ps[0][1][l]>v:
                if l+1<len(ps[0][1]) and ps[0][0]+ps[0][1][l+1]<=v:
                    break
                l+=1
            if l==len(ps[0][1]) or ps[0][0]+ps[0][1][l]>v:
                break
            while r<len(ps[2][1]) and ps[2][1][r]<v+ps[1][1][0]:
                r+=1
            if r==len(ps[2][1]) or ps[2][1][r]<v+ps[1][1][0]:
                break
            tmp=ps[2][1][r]+ps[2][0]-ps[0][1][l]
            if ans<tmp:
                ans=tmp
        return ans if ans!=-inf else 0



if __name__=='__main__':
    Solution().run()                                                                                                                                                                                                                                                                                                                                                                