import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Line, Bar
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


def gui1(v):
    ab_max = max([abs(d) for d in v])
    if ab_max == 0:
        return [0] * len(v)
    else:
        return [d / ab_max for d in v]


class EChart:
    def __init__(self):
        self.datas = []
        self.gui1 = False
        self.x_values = None

    def add_data(self, data):
        self.datas.append(data)
        return self

    def get_opts(self):
        return opts.InitOpts("100%", "900px", theme=ThemeType.LIGHT)

    def draw_lines(self):
        self.ins = Line(self.get_opts())
        if self.x_values is None:
            x_values = list(range(len(self.datas)))
        datas = lines_data(self.datas)
        self.ins.add_xaxis(x_values)
        for k, v in datas.items():
            if self.gui1:
                v = gui1(v)
            self.ins.add_yaxis(k, v, label_opts=opts.LabelOpts(is_show=False))
        return self

    def draw_bars(self, values):
        self.ins = (
            Bar(self.get_opts())
            .add_xaxis([1, 2, 3, 4, 5])
            .add_yaxis("y", values, stack="stack1", category_gap="50%")
        )

        # .set_series_opts(
        #     label_opts=opts.LabelOpts(
        #         position="right",
        #         formatter=JsCode(
        #             "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
        #         ),
        #     )
        # )

    def save(self, path):
        return self.ins.render(path)
