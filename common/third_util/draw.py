import json
import sys
import matplotlib.pyplot as plt
from common.util.export import List, defaultdict, File


def lines_data(datas):
    if isinstance(datas[0], dict):
        tmp_data = defaultdict(list)
        lines = []
        for data in datas:
            for k, v in data.items():
                tmp_data[k].append(v)
        for k, values in tmp_data.items():
            lines.append([values, None, k])


class Draw:
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()

    def draw_bar_chart(self, lines):
        self.ax.bar([l[0] for l in lines], [l[1] for l in lines])
        return self

    def draw_line(self, datas, xlabel="x", ylabel="y", title="title"):
        if isinstance(datas, dict):
            plt.plot(datas["x"], datas["y"], label=datas.get(title, ""))
        elif isinstance(datas, list):
            plt.plot(range(len(datas)), datas, label=title)
        else:
            raise Exception(datas)
        return self.show_line(xlabel, ylabel, title)

    def draw_lines(self, datas: List, xlabel="x", ylabel="y", title="title"):
        lines = datas

        for y, x, ti in lines:
            x = x or range(len(y))
            plt.plot(x, y, label=ti)
        return self.show_line(xlabel, ylabel, title)

    def show_line(self, xlabel, ylabel, title):
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.legend()
        return self

    def draw_graph(self, datas):
        import networkx as nx

        plt.figure(figsize=(8, 8))
        g = nx.DiGraph()
        nodes = []
        edges = dict()
        for f, t in datas:
            edges[(f, t)] = f"{f}_{t}"
            nodes.append((f, t))
        g.add_edges_from(nodes)
        pos = nx.layout.spring_layout(g, iterations=1, seed=227)
        nx.draw(
            g,
            pos,
            node_color="#aaa",
            node_shape="s",
            with_labels=True,
            node_size=800,
            alpha=1,
        )
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edges, font_color="#000")
        return self

    def draw_net_work2(self, input_data, out_put_path):
        import graphviz
        from graphviz import nohtml

        if isinstance(input_data, str):
            input_data = json.load(open(input_data, "r", encoding="utf-8"))
        g = graphviz.Digraph(
            "g", filename=out_put_path, node_attr={"shape": "record", "height": ".1"}
        )
        g.attr(rankdir="LR")
        node_map = dict()

        def get_node(key):
            if key not in node_map:
                node_map[key] = g.node(key, label=key, fontname="Microsoft YaHei")
            return node_map[key]

        def add_edge(f, t, label=""):
            g.edge(f, t, label=label)

        for k, v in input_data.items():
            get_node(k)
            for e in v:
                k1, *args = e.split(":")
                get_node(k1)
                add_edge(k, k1, *args)
        g.render(format="png")

    def save(self, path):
        File(path).make_dir_if_not_exist()
        plt.savefig(path)
        return self

    def draw_graph(self, path: str):
        out_put = path.replace(".json", "")
        data = {}
        with open(path, "r", encoding="utf-8") as f:
            data.update(json.loads(f.read()))
        self.draw_net_work2(data, out_put)

    def show(self):
        plt.show()
        return self
