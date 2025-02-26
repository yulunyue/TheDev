from common.util.test import TestBase
from common.algo.math_util import *
from common.algo.str_util import *
from common.algo.segtree import *
from common.algo.graph import *
import math
import json


class TestAlgo(TestBase):
    def test_graph(self):
        pass

    def test_util(self):
        self.expect(sin(90), 1)
        self.expect(cos(180), -1)
        for i in range(0, 361, 45):
            self.expect(int(calc_angle(
                0, 0, 3*sin(i), 3*cos(i)
            )/math.pi*180), i, i)


    def test_math(self):
        self.expect(bei_zen([2,3,4,5,7,8,9],2),None)

    def test_loop(self):
        for i in range(10**9):
            pass


    def test_seg_tree(self):
        pass

if __name__ == "__main__":
    TestAlgo().run()
