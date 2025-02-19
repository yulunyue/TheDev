
from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
null,true,false=None,True,False
class WordDictionary(SolutionBase):
    uri='https://leetcode.cn/problems/design-add-and-search-words-data-structure/description/'
    def get_cases(self):
        return [
            dict(
                mathods=["WordDictionary","addWord","addWord","search","search","search","search","search","search"],
                params=[[],["a"],["a"],["."],["a"],["aa"],["a"],[".a"],["a."]],
                result=[null,null,null,true,true,false,true,false,false]
            )
        ]
    def __init__(self):
        self.w=dict()

    def addWord(self, word: str) -> None:
        t=self.w
        for w in word:
            if w not in t:
                t[w]=dict()
            t=t[w]
        t["aa"]=1
    def search(self,s):
        q=[[0,self.w]]
        while q:
            i,t=q.pop(0)
            if 'aa' in t and i==len(s):
                return True
            if i==len(s):
                return False
            if s[i] in t:
                q.append([i+1,t[s[i]]])
            elif s[i]=='.':
                q.extend([[i+1,t[v]] for v in t if v!='aa'])
        return False

if __name__=="__main__":
    WordDictionary().run_cls()
            
