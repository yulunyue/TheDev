'''
https://leetcode.cn/problems/design-add-and-search-words-data-structure/description/
'''

class WordDictionary:

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
            if 'aa' in t:
                return True
            if i==len(s):
                return False
            if s[i] in t:
                q.append([i+1,t[s[i]]])
            elif s[i]=='.':
                q.extend([[i+1,t[v]] for v in t])
        return False
            
