from common.util.export import ApiBase, File, Node, Module, MockCf

ROOT = File("app/yly/algo")


class Algo(ApiBase):
    def search(self, **kw):
        nodes = []
        for f in ROOT.list_tree_file():
            if not f.name.endswith(".py"):
                continue

        return Node(childs=nodes)
