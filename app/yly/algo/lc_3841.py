from common.util.export import List, true, false, MockCf
from common.algo.base.tree.hld import HLD, SegTreeNode, HeavyNode
import string

MK = {v: 1 << (ord(v) - ord("a")) for v in string.ascii_lowercase}


class T(SegTreeNode):
    value = 0

    def do(self, v):
        self.value ^= v

    def merge(self, lv, rv):
        return lv ^ rv


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
        s2 = list(s)
        nodes = HeavyNode.load_from_edges(edges)
        root = nodes[0]
        h = HLD().set_root(root)
        t = T().set_range(0, h.timer - 1)
        h.set_seg(t)
        for i, v in enumerate(s):
            h.update_subtree(nodes[i], MK[v])
        ret = []
        for s in queries:
            m, p, d = s.split(" ")
            p = int(p)
            if m == "query":
                self.logger.map(s=s, s2=s2, t=t.print())
                v: int = h.query_path(nodes[p], nodes[int(d)], 0)
                ret.append(v.bit_count() <= 1)
            else:
                h.update_subtree(nodes[p], MK[s2[p]])
                self.logger.map(s=s, s2=s2, t=t.print())
                s2[p] = d
                h.update_subtree(nodes[p], MK[d])
                self.logger.map(s=s, s2=s2, t=t.print())

        return ret

    execute = palindromePath
