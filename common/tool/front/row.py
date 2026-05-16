class Row:
    type = "row"

    def __init__(self):
        self.childs = []

    def add(self, c):
        self.childs.append(c)
        return self

    def get_childs(self):
        return self.childs

    def to_json(self):
        return dict(
            type=self.type,
            children=self.get_childs(),
        )
