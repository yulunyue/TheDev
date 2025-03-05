# Definition for a binary tree node.
from typing import Optional,List,Dict
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        def dfs(n:TreeNode):
            if n is None:
                return 0,0
            l1,l2=dfs(n.left)
            r1,r2=dfs(n.right)
            return l2+r2,n.val+l1+r1
        return max(dfs(root))
