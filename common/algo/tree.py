from typing import List


class TreeNode:
    def __init__(self, val=0, *args, **kwargs):
        self.val = val
        self.childs = []

    @property
    def left(self):
        if len(self.childs):
            return self.childs[0]

    @property
    def right(self):
        if len(self.childs):
            return self.childs[-1]
