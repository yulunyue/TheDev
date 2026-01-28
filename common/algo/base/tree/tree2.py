class TreeNode:
    r"""
               A                #
          /    |  \             #
       B       C     D          #
     / | \    / \   / \         #
    E  F  G  H   I  J  K        #
    """

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left: TreeNode = left
        self.right: TreeNode = right

    def dfs(self, call):
        def util(n: TreeNode, depth=0):
            if n is None:
                return
            util(n.left, depth + 1)
            call(n, depth)
            util(n.right, depth + 1)

        util(self)

    @staticmethod
    def make(array):
        ans = [None] + [TreeNode(v) if v is not None else v for v in array]
        for i in range(1, len(ans)):
            if ans[i] is None:
                continue
            if i * 2 < len(ans):
                ans[i].left = ans[i * 2]
            if i * 2 + 1 < len(ans):
                ans[i].right = ans[i * 2 + 1]
        return ans[1]

    def show(self):
        ans = ["", "---TreeNode--begin--"]

        def util(n: TreeNode, depth):
            ans.append(f"{' '*depth*2}{n.val}: ")

        self.dfs(util)
        return "\n".join(ans + ["---TreeNode--end--", ""])
