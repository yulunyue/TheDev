import pandas as pd

from common.util.export import List, File, TempFile


class PandasUtil:
    def load(self, path: str):
        self.path = path
        if path.endswith(".shp"):
            import geopandas as gp

            self.instance = gp.read_file(path)
        else:
            self.instance = pd.read_excel(path, sheet_name="Sheet1")
        return self

    def info(self):
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
