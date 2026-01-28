try:
    import pygraphviz as pgv
except Exception:
    import graphviz as pgv
from common.util.export import File, logger


class PyGraphViz:
    def load(self, f: File):
        self.f = f.make_dir_if_not_exist()
        self.node_map = dict()
        self.g = pgv.AGraph(strict=False)
        self.g.attr(rankdir="LR")
        self.g.add_edge("a", "b", label="first")
        self.g.add_edge("a", "b", label="second")

    def save(self):
        self.g.layout()
        self.g.draw(self.f.path)

    def get_node(self, key):
        if key not in self.node_map:
            self.node_map[key] = self.g.node(key, label=key, fontname="Microsoft YaHei")
        return self.node_map[key]

    def draw_net_work(self, nodes, edges):
        self.node_config = nodes

        for k, v in input_data.items():
            get_node(k)
            for e in v:
                k1, *args = e.split(":")
                get_node(k1)
                add_edge(k, k1, *args)
