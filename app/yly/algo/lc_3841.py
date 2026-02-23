from common.util.export import List, true, false, MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            dict(
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
        pass
