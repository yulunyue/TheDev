from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf
class Solution(SolutionBase):
    def get_cases(self):
        return [
            # dict(s='121147',result=0),
            dict(s='5701283',result=18),
        ]
    
    def countSubstrings(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
    def execute(self,s:str):
        ans=0
        cnt={3:[1]+[0]*2,7:[1]+[0]*6,9:[1]+[0]*8}
        p7,b7=0,1
        cur=0
        s=[int(v) for v in s]
        for i,v in enumerate(s):
            cur+=v 
            p7=(p7*10+v)%7
            b7=(b7*10)%7
            d7=pow(b7,-1,7)
            m7=(p7*d7)%7
            #self.log_vals(locals(),f'v,p7,b7,d7,m7',cnt[7][m7])
            if v==1 or v==2 or v==5:
                ans+=i+1
            elif v==4:
                ans+=1
                if i>0 and s[i-1]%2==0:
                    ans+=i
            elif v==8:
                ans+=1
                if i>=2 and (s[i-2]*10+s[i-1])%4==0:
                    ans+=i-1
                if i and s[i-1]%4==0:
                    ans+=1
            elif v==3 or v==6:
                ans+=cnt[3][cur%3]
            elif v==9:
                ans+=cnt[9][cur%9]
            elif v==7:
                ans+=cnt[7][m7]
            cnt[3][cur%3]+=1
            cnt[7][m7]+=1
            cnt[9][cur%9]+=1
            

        return ans
        



if __name__=='__main__':
    Solution().run()