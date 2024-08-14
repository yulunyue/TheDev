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

    def manacher_get_odd_p(self):
        n = len(self.s)
        ret = [0]*n
        l, r = 0, -1
        for i in range(n):
            if i > r:
                k = 1
            else:
                k = min(ret[l+r-i], r-i+1)
            while k <= i and i+k < n and self.s[i-k] == self.s[i+k]:
                k += 1
            ret[i] = k
            k -= 1
            if i+k > r:
                l = i-k
                r = i+k
        return ret
