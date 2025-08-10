import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker
from collections import defaultdict
from typing import List, Dict


def lines_data(datas):
    tmp_data = defaultdict(list)
    if isinstance(datas[0], dict):
        for data in datas:
            for k, v in data.items():
                tmp_data[k].append(v)
    return tmp_data


class EChart:

    def draw_lines(self, datas: List[dict], x_values=None, gui1=False):
        self.ins = Line(opts.InitOpts("100%", "660px"))
        if x_values is None:
            x_values = list(range(len(datas)))
        datas = lines_data(datas)
        self.ins.add_xaxis(x_values)
        for k, v in datas.items():

            if gui1:
                ab_max = max([abs(d) for d in v])
                if ab_max == 0:
                    v = [0] * len(v)
                else:
                    v = [d / ab_max for d in v]
            self.ins.add_yaxis(k, v, label_opts=opts.LabelOpts(is_show=False))
        return self

    def save(self, path):
        return self.ins.render(path)
