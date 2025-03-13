from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(word="aeiou",k=0,result=1),
            dict(word="iqeaouqi",k=2,result=3)
        ]
    def execute(self, word: str, k: int) -> int:
        kc=[]
        o=dict(a=0,e=0,i=0,o=0,u=0)
        l=on=ans=0
        last_l=-1
        for r,v in enumerate(word):
            v=word[r]
            if v in o:
                on+=o[v]==0
                o[v]+=1
            else:
                kc.append(r)
            while l<r and on==5:
                if word[l] in o:
                    if o[word[l]]==1:
                        break
                    o[word[l]]-=1
                l+=1
            if len(kc)>=k:
                if len(kc)>k:
                    last_l=kc.pop(0)
                if on==5:
                    ans+=max(min(l,kc[0] if kc else l)-last_l,0)
                    self.log(word[l:r+1],last_l,l,ans)            
        return ans
    def countOfSubstrings(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)



if __name__=='__main__':
    Solution().run()