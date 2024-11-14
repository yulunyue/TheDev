
from common.algo.absearch import AlphaBateSearch, AbNode
import sys
from app.yly.algo.manage import SolutionBase
TREE1 = '''
a: 4
  b:
    f:
      o: 8
      p: 9
    g: 2
    h: 7
  c:
    i: 1
    j: 1
    k: 4
  d:
    l: 3
    m: 6
    n: 9
  e: 2
'''


class Solution(SolutionBase):

    def get_cases(self):
        return [
            dict(root=TREE1, result="")
        ]

    def init(self, root, **kw):
        self.root = AbNode("").load_from_yml(root)
        self.ab = AlphaBateSearch()

    def get_watch(self):
        return [
            # self.watch("tree", self.root)
        ]

    def execute(self):
        return self.ab.search(last_move=self.root)[1]


if __name__ == '__main__':
    Solution().run()
