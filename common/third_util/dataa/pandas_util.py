import pandas as pd

from common.util.export import List, File, TempFile


class PandasUtil:
    @classmethod
    def is_excel_file(cls, name):
        return name in {"xlsx"}

    def dump_json(self):
        File(self.path + ".json").write_file(self.to_json())

    def load(self, path: str):
        self.path = path
        self.instance = pd.read_excel(path)
        return self

    def get_info(self):
        f = TempFile(TempFile.STR_MODE)
        self.instance.info(buf=f)
        return f.data

    def group_by(self, *keys):
        ret = dict()
        for index, row in self.instance.iterrows():
            k = "|".join(row[key] for key in keys)
            ret[k] = ret.get(k, 0) + 1
        return ret

    def head(self, n="1"):
        return self.instance.head(int(n))

    def hander(self, method, *args):
        return getattr(self, method)(*args)

    def to_json(self):
        return self.instance.to_json(force_ascii=False, orient="columns")
