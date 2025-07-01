from typing import Dict
from common.service.http import Node
from common.util.fp import File


class Route:
    prefix = ""

    def get_file(self, path, **kw):
        return File(self.prefix + path)

    def read(self, path="", **kw):
        value = self.get_file(path).read_file()
        if isinstance(value, dict):
            return Node().set_data(**value)
        return Node().set_value(value)

    def check(self, **kw):
        pass

    def save_all(self, path="", **kw):
        self.get_file(path).write_file(kw)
        return Node()

    def save_one(self, **kw):
        pass

    def add(self, **kw):
        pass

    def get(self, **kw):
        return self.read(**kw)
