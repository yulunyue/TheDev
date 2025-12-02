import pytest


class PyTestUtil:
    def __init__(self):
        self.flag_map = dict()
        self.flags = ["-vs", "--full-trace", "--json-report"]

    def set_root(self, path):
        self.flag_map["--rootdir"] = path
        return self

    def set_flags(self, *args):
        self.flags.extend(args)
        return self

    def main(self):
        flags = self.flags[:]
        for k, v in self.flag_map.items():
            flags.extend([k, v])
        pytest.main(flags)
