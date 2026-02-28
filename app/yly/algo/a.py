from common.util.export import MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(s="zbayyz", k=4, result="zbay"),
        )

    def mergeCharacters(self, s: str, k: int) -> str:
        s = list(s)
        i, j = 0, 1
        while i < len(s):
            j = i + 1
            c = 0
            while j < len(s) and i < len(s) and j <= i + k:
                if s[j] == s[i]:
                    s.pop(j)
                    c = k
                    continue
                j += 1
            self.logger.map(i=i, s=s)
            i = max(0, i + 1 - c)

        return "".join(s)

    execute = mergeCharacters
