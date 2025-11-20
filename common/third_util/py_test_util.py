import pytest


class PyTestUtil:
    def __init__(self):
        self.flags = ["-vs", "--full-trace", "--json-report"]

    def set_flags(self, *args):
        self.flags.extend(args)
        return self

    def main(self):
        pytest.main(self.flags)
