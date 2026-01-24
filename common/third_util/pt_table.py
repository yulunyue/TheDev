from prettytable import PrettyTable
from typing import Dict, List
from common.tool.export import ConfigBase
from common.util.log import logger


class PtTable:
    def __init__(self):
        self.pr = PrettyTable(float_format=".3")

    def load_form_model(self, c: ConfigBase):
        self.pr.field_names = c.get_headers()
        for row in c.get_row_datas():
            self.pr.add_row(row)
        return self

    def load_from_matrix(self, matrix, titles=None):
        if titles is None:
            titles = list(range(len(matrix[0])))
        self.pr.field_names = titles
        for m in matrix:
            self.pr.add_row(m)
        return self

    def show(self):
        return "\n" + str(self.pr) + "\n"
