try:
    import pygraphviz as pgv
except Exception:
    import graphviz as pgv
from common.util.export import File, logger


class PyGraphViz:
    def load(self, f: File):
        if isinstance(f, str):
            self.f = File(f)
        else:
            self.f = f.make_dir_if_not_exist()
        self.node_map = dict()
        self.edges_map = dict()
        self.g: pgv.AGraph = pgv.AGraph(strict=True)

        # self.g.attr(rankdir="LR")
        return self

    def add_edge(self, f, t, v):
        k = f, t
        if k not in self.edges_map:
            self.edges_map[k] = self.g.add_edge(f, t, label=str(v))
        return self.edges_map[k]

    def save(self):
        logger.info(self.f)
        self.g.layout()
        self.g.draw(self.f.path)

    def add_node(self, key):
        if key not in self.node_map:
            label = key
            if key in self.node_config:
                label = f"{key}:{self.node_config[key]}"
            self.node_map[key] = self.g.add_node(
                key, label=label, fontname="Microsoft YaHei"
            )
        return self.node_map[key]

    def draw(self, nodes, edges):
        self.node_config = nodes
        for k in nodes:
            self.add_node(k)
        for f, t, *args in edges:
            self.add_edge(f, t, *args)
        self.save()
