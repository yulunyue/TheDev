class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    @staticmethod
    def load_from_edges(self, nums, edges):
        nodes=[TreeNode(n) for n in nums]
        for p,n in enumerate(edges):
            pass