import pandas as pd
import geopandas as gp


class PandasUtil:
    def __init__(self, path: str):
        if path.endswith(".shp"):
            self.instance = gp.read_file(path)
