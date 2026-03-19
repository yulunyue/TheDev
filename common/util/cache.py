from .fp import File
from typing import Dict


class Cache:
    def __init__(self, name):
        self.fp = File(f"data/cache/{name}.json")
        self.store = dict()
        if self.fp.exists():
            self.store.update(self.fp.read_file())

    def set(self, key, value):
        self.store[key] = value
        return self

    def get(self, key):
        return self.store[key]

    def exists(self, key):
        return key in self.store

    def save(self):
        self.fp.write_file(self.store)
        return self


CACHE: Dict[str, Cache] = dict()


def get_cache(name):
    if name not in CACHE:
        CACHE[name] = Cache(name)
    return CACHE[name]
