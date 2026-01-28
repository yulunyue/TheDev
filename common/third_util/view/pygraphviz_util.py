import pygraphviz as pgv
from common.util.export import File, logger


class PyGraphViz:
    def __init__(self):
        self.g = pgv.AGraph(strict=False)
        self.g.add_edge("a", "b", label="first")
        self.g.add_edge("a", "b", label="second")

    def save(self):
        self.g.layout()
        f = File("data/view/advanced_topology.png")
        logger.info(f.make_dir_if_not_exist())
        self.g.draw(f.path)
