import yaml
import json
from typing import List


def merge_list(src: list, dst, key, keys, check):
    ks = {s[key]: s for s in src}
    for d in dst:
        if d[key] not in ks:
            ks[d[key]] = d
            src.append(d)
        else:
            diff_json(ks[d[key]], d, keys + [d[key]], check)
    return src


def diff_json(src, dst, keys, check):
    if isinstance(src, dict) and isinstance(dst, dict):
        for key, v in dst.items():
            k = keys + [key]
            if key not in src:
                src[key] = check(k, None, v, "insert")
            else:
                src[key] = diff_json(src[key], v, k, check)
        return
    elif isinstance(src, (str, int, bool)) and isinstance(dst, (str, int, bool)):
        if src != dst:
            return check(keys, src, dst, "update")
        return src
    return check(keys, src, dst, "unnone")


class BaseDiff:
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            self.lines = f.read().split("\n")
        return self

    def get_lines(self):
        return self.lines

    def get_output(self):
        return "\n".join(self.lines)

    def merge(self, path, *args):
        return self

    def set_info(self, info, local_path):
        self.info = info
        self.local_path = local_path
        self.need_merge: List[BaseDiff] = []
        return self


class JsonDiff(BaseDiff):
    def load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            self.data = json.loads(f.read())
        return self

    def get_output(self):
        return json.dumps(self.data, ensure_ascii=False, indent=4)

    def merge(self, p, util):
        diff_json(self.data, p.data, [], util)
        return self


class YmlDiff(BaseDiff):
    def load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)
        return self

    def get_output(self):
        class F:
            data = ""

            @staticmethod
            def write(data):
                F.data += data

            @staticmethod
            def flush():
                pass

        yaml.safe_dump(self.data, F, allow_unicode=True)
        return F.data

    def merge(self, p, util):
        diff_json(self.data, p.data, [], util)
        return self
