from typing import List


class StrUtil:
    def __init__(self, s):
        self.s: str = s

    def str_prefix_match(self, prefixs: List[str]):
        for p in prefixs:
            if self.s.startswith(p):
                return True
        return False

    def format_pre0_bin(self, n):
        return format(self.s, f"0{n}b")
