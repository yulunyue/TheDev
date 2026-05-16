from common.util.fp import File
import json
from common.util.tool import hash_any_str


class TsFile:
    PREFIX = "let DATA="

    def __init__(self) -> None:
        self.config = dict()

    def load(self, path):
        self.fp = File(path)
        if not self.fp.exists():
            self.fp.write_file(self.get_content())
        else:
            self.load_content()
        return self

    def get_content(self):
        return f"{TsFile.PREFIX}{json.dumps(self.config)}\nexport default DATA"

    def load_content(self):
        self.config = json.loads(
            self.fp.read_file().split("\n")[0][len(TsFile.PREFIX) :]
        )

    def set(self, keys, value):
        tmp = self.config
        for key in keys[:-1]:
            tmp[key] = tmp.get(key, dict())
            tmp = tmp[key]
        tmp[keys[-1]] = value
        self.fp.write_file(self.get_content())

    def get(self, keys, defalt_value=None):
        tmp = self.config
        for key in keys[:-1]:
            tmp = tmp.get(key, dict())
        return tmp.get(keys[-1], defalt_value)

    def update_api(self, path, param, data):
        self.set([path, hash_any_str(param)], data)

    def test(self):
        self.load("data/test/a.ts")
        self.set(["a", "b"], self.get(["a", "b"], 0) + 1)


if __name__ == "__main__":
    TsFile().test()
