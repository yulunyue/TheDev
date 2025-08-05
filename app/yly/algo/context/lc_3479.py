from common.util.export import List
from common.algo.base.segtree import SegTreeNode


class St(SegTreeNode):
    pass


class Solution:
    def get_cases(self):
        return [dict(fruits=[4, 2, 5], baskets=[3, 5, 4], result=1)]

    def execute(self, *args, **kw):
        return self.numOfUnplacedFruits(**kw)

    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        n = len(baskets)
        s = St().set_range(0, n - 1).build(baskets)
