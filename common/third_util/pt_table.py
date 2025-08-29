from prettytable import PrettyTable
from typing import Dict, List


class TableModel:
    _STORE: Dict[str, "TableModel"] = dict()
    _headers = None

    def __init__(self, key):
        self.key = key

    def __new__(cls, key):
        if key in cls._STORE:
            return cls._STORE[key]
        cls._STORE[key] = object.__new__(cls)
        return cls._STORE[key]

    @classmethod
    def get_headers(cls):
        if cls._headers is not None:
            return cls._headers
        cls._headers = []
        for k in dir(cls):
            if k.startswith("_") or k == "key":
                continue
            v = getattr(cls, k)
            if isinstance(v, (str, int, float)):
                cls._headers.append(k)
        cls._headers.sort()
        cls._headers.insert(0, "key")
        return cls._headers

    @classmethod
    def get_row_datas(cls):
        ret = []
        for v in sorted(cls._STORE.values(), key=cls.sort):
            tmp = []
            for k in cls.get_headers():
                tmp.append(getattr(v, k))
            ret.append(tmp)
        return ret

    @classmethod
    def sort(cls, v: "TableModel"):
        return [getattr(v, u) for u in cls.get_headers()[1:]]

    @classmethod
    def clear(cls):
        cls._STORE = dict()


class PtTable:
    def __init__(self):
        self.pr = PrettyTable()

    def load_form_model(self, c: TableModel):
        self.pr.field_names = c.get_headers()
        for row in c.get_row_datas():
            self.pr.add_row(row)
        return self

    def load_from_matrix(self, matrix, titles=None):
        if titles:
            self.pr.field_names = titles
        for m in matrix:
            self.pr.add_row(m)
        return self

    def __str__(self):
        return str(self.pr)
