from common.util.export import List


class Solution:
    def get_cases(self):
        return [
            dict(
                nums=[1, 1, 2, 2, 1, 1],
                queries=[[0, 5, 4], [0, 3, 3], [2, 3, 2]],
                result=[1, -1, 2],
            )
        ]

    def subarrayMajority(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        ct = dict()
