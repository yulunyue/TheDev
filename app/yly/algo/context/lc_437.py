# Definition for a binary tree node.

from common.util.export import Optional, null, defaultdict, logger
from common.algo.base.node import TreeNode


class Solution:
    def get_cases(self):
        return [
            # dict(
            #     root=TreeNode.make([10, 5, -3, 3, 2, null, 11, 3, -2, null, 1]),
            #     targetSum=8,
            #     result=3,
            # ),
            dict(
                root=TreeNode.make([5, 4, 8, 11, null, 13, 4, 7, 2, null, null, 5, 1]),
                targetSum=22,
                result=3,
            ),
        ]

    def pathSum(self, root: TreeNode, targetSum: int) -> int:
        mp = defaultdict(int)
        mp[0] = 1
        self.ans = 0

        def dfs(n: TreeNode, pre_sum):
            if n is None:
                return
            pre_sum += n.val
            mp[pre_sum] += 1
            self.ans += mp[pre_sum - targetSum]
            # logger.map(ans=self.ans, val=n.val, pre_sum=pre_sum, mp=dict(mp))
            dfs(n.left, pre_sum)
            dfs(n.right, pre_sum)
            mp[pre_sum] -= 1

        dfs(root, 0)
        return self.ans

    execute = pathSum
