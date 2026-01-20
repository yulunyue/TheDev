from common.util.export import List, defaultdict


class Solution:
    def get_cases(self):
        return dict(case0=dict(s="aaccb", result="aacb"))

    def lexSmallestAfterDeletion(self, s: str) -> str:
        """ """
        ct = defaultdict(list)
        for i, v in enumerate(s):
            ct[v].append(i)

    execute = lexSmallestAfterDeletion
