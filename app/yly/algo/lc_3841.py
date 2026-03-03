from common.util.export import List, true, false, MockCf, true, false, TheDevLoger
from common.algo.base.tree.hld import HLD, SegTreeNode, HeavyNode
import string

MK = {v: 1 << (ord(v) - ord("a")) for v in string.ascii_lowercase}


class T(SegTreeNode):
    h: HLD = None
    s = []
    logger: TheDevLoger = None

    def load(self, s):
        self.value = MK[s[T.h.rnk[self.l].key]]

    def do(self, v):
        self.value ^= v

    def merge(self, lv, rv):
        return lv ^ rv

    def show(self):
        return f"{T.h.rnk[self.l].key}-{T.h.rnk[self.r].key} v:{self.value}"


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case1=dict(
                n=3,
                edges=[[0, 1], [1, 2]],
                s="aac",
                queries=["query 0 2", "update 1 b", "query 0 2"],
                result=[true, false],
            ),
            case2=dict(
                n=4,
                edges=[[0, 1], [0, 2], [0, 3]],
                s="abca",
                queries=[
                    "query 1 2",
                    "update 0 b",
                    "query 2 3",
                    "update 3 a",
                    "query 1 3",
                ],
                result=[false, false, true],
            ),
            case0=dict(
                n=3,
                edges=[[0, 2], [0, 1]],
                s="ghh",
                queries=["query 1 2"],
                result=[true],
            ),
        )

    def palindromePath(
        self, n: int, edges: list[list[int]], s: str, queries: list[str]
    ) -> list[bool]:
        T.s = s2 = list(s)
        T.logger = self.logger
        nodes = HeavyNode.load_from_edges(edges)

        root = nodes[0]
        h = T.h = HLD().set_root(root)
        self.logger.info(root.show())
        t = T().set_range(0, n - 1).build(s)
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
