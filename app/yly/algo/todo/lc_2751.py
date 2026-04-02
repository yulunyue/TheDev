from common.util.export import List, MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(
                positions=[5, 4, 3, 2, 1],
                healths=[2, 17, 9, 15, 10],
                directions="RRRRR",
                result=[2, 17, 9, 15, 10],
            )
        )

    def survivedRobotsHealths(
        self, positions: List[int], healths: List[int], directions: str
    ) -> List[int]:
        pass
