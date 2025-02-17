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
        self.expect(math.gcd(12), [])

    def test_loop(self):
        for i in range(10**9):
            pass

    def test_inter_tree(self):
        s = IntervalTreeNode(10, 0)
        s.add_value(3, 1)
        s.add_value(5, 2)
        self.expect(s.query_sum(6)-s.query_sum(2), 3)
        self.expect(s.query_sum(6)-s.query_sum(4), 2)

    def test_seg_tree(self):
        pass

    def test_alphabate(self):
        self.expect(AlphaBate(2).search(), 3)

    def test_str(self):
        a="ababcaba"
        self.expect(kmp_array(a),[-1,0,1,2,0,1,2,3])

if __name__ == "__main__":
    TestAlgo().run()
