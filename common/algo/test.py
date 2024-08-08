from common.util.test import TestBase
from common.algo.util import *
from common.algo.str_util import *
from common.algo.segtree import *
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
        self.expect(
            list(combinations([1, 2, 3], 2)),
            [(1, 2), (1, 3), (2, 3)]
        )
        self.expect(
            list(permutations([1, 2, 3], 2)),
            [(1, 2), (1, 3), (2, 3)]
        )

    def test_math(self):
        self.expect(math.gcd(12), [])

    def test_loop(self):
        for i in range(10**9):
            pass

    def test_str(self):
        self.expect(
            Manacher("aababab").get_odd_p(),
            [1, 1, 2, 3, 3, 2, 1]
        )

    def test_inter_tree(self):
        s = IntervalTree(10, 0)
        s.add_value(3, 1)
        s.add_value(5, 2)
        self.expect(s.query_sum(6)-s.query_sum(2), 3)
        self.expect(s.query_sum(6)-s.query_sum(4), 2)

    def test_seg_tree(self):
        s = SegTree(6)
        s.update_min(2, 5, 2)
        s.update_min(4, 5, 3)
        c = s.query_min(1, 4)
        print(json.dumps(s.info(), indent=4))
        self.expect(c, 2)
        # self.expect(s.query_min(5, 5), 3)


if __name__ == "__main__":
    TestAlgo().run()
