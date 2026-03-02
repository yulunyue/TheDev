from common.util.export import List, true, false, MockCf
from common.algo.base.tree.hld import HLD, SegTreeNode, HeavyNode
import string

MK = {v: 1 << (ord(v) - ord("a")) for v in string.ascii_lowercase}


class T(SegTreeNode):
    h: HLD = None
    s = []

    def load(self, s):
        self.value = MK[s[self.l]]

    def do(self, v):
        self.value ^= v

    def merge(self, lv, rv):
        return lv ^ rv

    def show(self):
        return f"{T.h.rnk[self.l].key}-{T.h.rnk[self.r].key} v:{self.value}"


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(
                n=3,
                edges=[[0, 1], [1, 2]],
                s="aac",
                queries=["query 0 2", "update 1 b", "query 0 2"],
                result=[true, false],
            ),
        )

    def palindromePath(
        self, n: int, edges: list[list[int]], s: str, queries: list[str]
    ) -> list[bool]:
        T.s = s2 = list(s)
        nodes = HeavyNode.load_from_edges(edges)
        root = nodes[0]
        h = T.h = HLD().set_root(root)
        t = T().set_range(0, h.timer - 1).build(s)
        h.set_seg(t)
        ret = []
        for s in queries:
            m, p, d = s.split(" ")
            p = int(p)
            if m == "query":
                self.logger.map(s=s, s2=s2, t=t.print())
                v: int = h.query_path(nodes[p], nodes[int(d)], 0)
                ret.append(v.bit_count() <= 1)
            else:
                h.update_path(nodes[p], nodes[p], MK[s2[p]])
                self.logger.map(s=s, s2=s2, t=t.print())
                s2[p] = d
                h.update_path(nodes[p], nodes[p], MK[d])
                self.logger.map(s=s, s2=s2, t=t.print())

        return ret

    execute = palindromePath
