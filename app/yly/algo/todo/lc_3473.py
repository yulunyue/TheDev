class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n,m=len(str1),len(str2)
        s=str2
        a=[""]*(n+m-1)
        b=["a"]*(n+m-1)
        c=dict(T=[],F=[])
        for i,v in enumerate(str1):
          c[v].append(i)
        for i in c["T"]:
          for j in range(m):
            k=i+j
            if a[k] and a[k]!=s[j]:
              return ""
            a[k]=b[k]=s[j]
        for i in c["F"]:
           f=-1
           for j in range(m):
             if not a[i+j]:
               f=i+j
             if b[i+j]!=s[j]:
               f=None
               break
           if f==-1:
             return ""
           if f is not None:
             b[f]="b"
        return "".join(b
                       str1 = "TFTF", str2 = "ab"

输出: "ababa")
