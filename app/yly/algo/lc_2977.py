from common.util.export import MockCf, List, defaultdict
from common.algo.base.graph.util import floyd
from common.algo.base.tree.tietree import TieNode


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(
                source="abcdefgh",
                target="acdeeghh",
                original=["bcd", "fgh", "thh"],
                changed=["cde", "thh", "ghh"],
                cost=[1, 3, 5],
                result=9,
            )
        )

    def minimumCost(
        self,
        source: str,
        target: str,
        original: List[str],
        changed: List[str],
        cost: List[int],
    ) -> int:
        ct = defaultdict(int)
        keys = set()
        for i, v in enumerate(original):
            ct[original[i], changed[i]] = cost[i]
            keys.update(original[i], changed[i])
        floyd(ct, keys)
        n = len(source)

    execute = minimumCost
