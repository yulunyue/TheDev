class StrUtil:
    def __init__(self,s) -> None:
        self.s=s

    def z_kmp(self):
        n=len(self.s)
        z=[0]*n
        l=r=0
        for i in range(1,n):
            z[i]=max(min(z[i-l],r-i+1),0)
            while i+z[i]<n and self.s[z[i]]==self.s[z[i]+i]:
                l,r=i,i+z[i]
                z[i]+=1
            
        return z