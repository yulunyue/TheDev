from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
from common.algo.segtree import SegTreeNode
class T(SegTreeNode):
    def do(self, v):
        self.value=v
    def up(self, *args):
        self.value=self.left.value+self.right.value
class NumArray(SolutionBase):
    uri='https://leetcode.cn/problems/game-of-life/'
    def get_cases(self):
        return [
            dict(
                methods=["NumArray", "sumRange", "update", "sumRange"],
params=[[[1, 3, 5]], [0, 2], [1, 2], [0, 2]],
result=[null, 9, null, 8])
        ]


    def __init__(self, nums: List[int]):
        self.t=T().set_range(0,len(nums)-1).build(
            lambda i:nums[i]
        )

    def update(self, index: int, val: int) -> None:
        self.t.update(index,index,val)

    def sumRange(self, left: int, right: int) -> int:
        return self.t.query_sum(left,right)



if __name__=='__main__':
    NumArray.run_cls()