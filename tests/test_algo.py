from common.util.export import TestBase, json, math, logger
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
    XorBarisDev as XorBais,
    Tree,
    GaussElimination,
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
        nodes = Tree.load_from_edges(
            [[0, 1], [0, 2], [1, 3], [3, 4], [3, 5], [5, 6], [6, 7]]
        )
        root = nodes[0].bei_zhen()
        self.expect(root.get_k_parent(nodes[7], 5).key, 0)
        self.expect(root.get_last_lcm_parent(nodes[4], nodes[7]).key, 3)

    def test_math(self):
        self.expect(math.comb(5, 3), 5 * 4 * 3 // (3 * 2 * 1))
        self.expect(sin(90), 1.0)
        self.expect(cos(180), -1.0)

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
        value = [1, 2, 1]
        pos = [1, 2, 1]
        s = encode_data(value, pos)
        self.expect(bin(s), "0b1101")
        self.expect(decode_data(s, pos), value)

    def test_xor_bias(self):
        xs = [5, 3, 4, 7, 9, 2, 11]
        xb = XorBais().set_b(xs)
        self.expect(xb.max_xor(), 15, xb)

    def test_ge(self):
        x = GaussElimination([[2, 1, 1], [6, 2, 1], [-2, 2, 1]], [1, -1, 7]).calc()
        self.expect(x, [-1.0, 2.0, 1.0])


if __name__ == "__main__":
    TestAlgo().run()
