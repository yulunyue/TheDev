from common.util.export import TestBase, json, math
from common.algo.export import (
    sin,
    cos,
    calc_angle,
    manacher_get_odd_p,
    get_sa_prefix_doubling,
    get_height_form_sa,
    LazyHeapMinMax,
    Comb,
    encode_data,
    decode_data,
)


class TestAlgo(TestBase):
    def test_tree(self, *args):
        """
           0
         1   2
         3
        4  5
           6
           7
        """
        nodes = TreeNode.load_from_edges(
            [[0, 1], [0, 2], [1, 3], [3, 4], [3, 5], [5, 6], [6, 7]]
        )
        root = nodes[0].bei_zhen()
        self.expect(nodes[7].parents[0].key, 6)
        self.expect(nodes[7].parents[1].key, 5)
        self.expect(nodes[7].parents[2].key, 1)
        self.expect(nodes[6].parents[2].key, 0)
        self.expect(root.get_k_parent(nodes[7], 5).key, 0)
        self.expect(root.get_last_lcm_parent(nodes[4], nodes[7]).key, 3)
        self.expect(root.get_dis2node(nodes[4], nodes[7]), 4)

    def test_math(self):
        self.expect(math.comb(5, 3), 5 * 4 * 3 / (3 * 2 * 1))
        self.expect(sin(90), 1)
        self.expect(cos(180), -1)
        for i in range(0, 361, 45):
            self.expect(
                int(calc_angle(0, 0, 3 * sin(i), 3 * cos(i)) / math.pi * 180), i, i
            )
        c = Comb().load(7, 6)
        self.expect(c.fac, []),

    def test_str(self):
        s = "aabcbc"
        hi, sa, rk = [0, 1, 0, 2, 0, 1], [0, 1, 4, 2, 5, 3], [0, 1, 3, 5, 2, 4]
        self.expect(
            manacher_get_odd_p(s),
            [0, 1, 2, 1, 0, 1, 0, 3, 0, 3, 0, 1, 0],
        )  #'a#a#b#c#b#c'
        self.expect(get_sa_prefix_doubling(s), (sa, rk))
        self.expect(get_height_form_sa(s)[0], hi)

    def test_bin(self):
        a = [1, 1, 1]
        p = [1, 2, 2]
        s = encode_data(a, p)
        self.expect(bin(s), "0b10101")
        self.expect(decode_data(s, p), a)


if __name__ == "__main__":
    TestAlgo().run()
