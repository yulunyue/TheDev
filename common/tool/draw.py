import json
import sys
import matplotlib.pyplot as plt


class Draw:
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()

    def draw_bar_chart(self, lines):
        self.ax.bar([l[0] for l in lines], [l[1] for l in lines])
        return self

    def draw_line(self, datas, xlabel="x", ylabel="y", title="title"):
        if isinstance(datas, dict):
            for k, dts in datas.items():
                x = datas.get("x", range(len(dts["y"])))
                plt.plot(x, dts["y"], label=k)
        elif isinstance(datas, list):
            plt.plot(range(len(datas)), datas, label=title)
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.legend()
        return self

    def draw_graph(self, datas):
        import matplotlib.pyplot as plt
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
        import matplotlib.pyplot as plt

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


if __name__ == "__main__":
    getattr(Draw(), sys.argv[1])(*sys.argv[2:])
