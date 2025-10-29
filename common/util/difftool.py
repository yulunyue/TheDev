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
        if (isinstance(src, float) or isinstance(dst, float)) and abs(
            src - dst
        ) <= 0.00001:
            return
        if str(src) == str(dst):
            return
        self.diff_result.append(
            f"update[{self.key_join_char.join(keys)}][{src}][{dst}]"
        )

    def is_same(self, dst):
        if isinstance(dst, str) and isinstance(self.src, (list, dict)):
            dst = json.loads(dst)
        if isinstance(self.src, str) and isinstance(dst, (list, dict)):
            self.src = json.loads(self.src)
        return "\n".join(self.compare(dst))

    def expect_ndarray(self, a, e, wucha=0.000001):
        from common.third_util.np_util import np

        if getattr(a, "requires_grad", False):
            a = a.detach().numpy()
        if not isinstance(a, np.ndarray):
            a = np.array(a)
        if not isinstance(e, np.ndarray):
            e = np.array(e)
        cha = 0
        if a.shape != e.shape:
            equ = False
        else:
            cha = abs(a - e).sum()
            equ = cha <= wucha
        if not equ:
            return f"shape:{a.shape}{a}", f"!=\nshape:{e.shape}{e}", f"cha:{cha}"
        return ""

    def diff_any(self, src, dst, keys):
        if src is None or dst is None:
            return "" if src is None and dst is None else f"{src}!={dst}"
        elif isinstance(src, dict) and isinstance(dst, dict):
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
                if key >= len(src):
                    self.insert(k, dst[key])
                elif key >= len(dst):
                    self.delete(k, src[key])
                else:
                    self.diff_any(src[key], dst[key], k)
        elif isinstance(src, (str, int, bool, float)) and isinstance(
            dst, (str, int, bool, float)
        ):
            self.diff(keys, src, dst)
        else:
            return self.expect_ndarray(src, dst)
