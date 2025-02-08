
# Definition for a Node.
from typing import Optional
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


class Solution:
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        s=[]
        def dfs(n:Node,dp=0):
            if n is None:
                return
            if dp==len(s):
                s.append([])
            s[dp].append(n)
            dfs(n.left)
            dfs(n.right)
        for ns in s:
            for i in range(len(ns)-1):
                ns[i].next=ns[i+1]
        dfs(root)
        return root