from typing import List


class StrUtil:
    def __init__(self):
        self.prefixs = []

    def str_prefix_match(self, s: str):
        for p in self.prefixs:
            if s.startswith(p):
                return True
        return False

    def format_pre0_bin(self, n):
        return format(self.s, f"0{n}b")

    def set_prefix(self, prefixs: List[str]):
        self.prefixs = prefixs
        return self

    def match(self):
        if self.str_prefix_match():
            return True
        return False
