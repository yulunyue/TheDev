from common.util.export import MockCf, List
from common.algo.base import bin_util


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
        pass
