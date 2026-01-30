from typing import List, Dict
from collections import defaultdict


class TieNode:

    def __init__(self):
        self.childs = dict()

    def add(self, k):
        tmp = self
        for i in s:
            if tmp.childs[i] is None:
                tmp.childs[i] = TieNode(
                    i,
                    self.keys,
                    depth=tmp.depth + 1,
                    default_value=self.default_value,
                    parent=self,
                    root=self,
                )
            tmp = tmp.childs[i]
        return tmp
