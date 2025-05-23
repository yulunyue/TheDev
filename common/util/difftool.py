import yaml
import json
from typing import List


class Diff:
    def __init__(self, src):
        self.src = src
        self.key_join_char = "/"

    def compare(self, dst):
        self.diff_result = []
        self.diff_any(self.src, dst, [])
        return self.diff_result

    def insert(self, keys, value):
        self.diff_result.append(f"insert[{self.key_join_char.join(keys)}][{value}]")

    def delete(self, keys, value):
        self.diff_result.append(f"delete[{self.key_join_char.join(keys)}][{value}]")

    def diff(self, keys, src, dst):
        if isinstance(src, float) and abs(src - dst) <= 0.0001:
            return
        if src == dst:
            return
        self.diff_result.append(
            f"update[{self.key_join_char.join(keys)}][{src}][{dst}]"
        )

    def diff_any(self, src, dst, keys):
        if isinstance(src, dict) and isinstance(dst, dict):
            for key in set(src.keys() + dst.keys()):
                k = keys + [key]
                if key not in src:
                    self.insert(k, dst[key])
                elif key not in dst:
                    self.delete(k, src[key])
                else:
                    self.diff_any(src[key], dst[key], k)
        elif isinstance(src, list) and isinstance(dst, list):
            for key in range(max(len(src), len(dst))):
                k = keys + [str(key)]
                if key > len(src):
                    self.insert(k, dst[key])
                elif key > len(dst):
                    self.delete(k, src[key])
                else:
                    self.diff_any(src[key], dst[key], k)
        elif isinstance(src, (str, int, bool, float)) and isinstance(
            dst, (str, int, bool, float)
        ):
            self.diff(keys, src, dst)
        else:
            raise Exception(f"can not diff {keys} {src} {dst}")
