from collections import defaultdict
class Solution:
    def maximumLength(self, s: str) -> int:
        sp=dict()
        for i,v in enumerate(s):
            if v not in sp:
                sp[v]=[[i,i]]
            elif sp[v][-1][-1]==i-1:
                sp[v][-1][-1]=i
            else:
                sp[v].append([i,i])
        ret=-1
        print(sp)
        for k,v in sp.items():
            sp2=[b-a+1 for a,b in v]
            vmax=max(sp2)
            vmin=min(sp2)
            if vmax>=3:
                ret=max(ret,vmax-2)
            if len(v)>=3:
                ret=max(ret,vmin)
            print(k,ret,sp2)
        return ret
                
if __name__=='__main__':
    print(Solution().maximumLength("aada"))