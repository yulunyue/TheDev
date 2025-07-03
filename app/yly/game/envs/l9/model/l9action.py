from common.algo.search.state import Action


class L9Action(Action):

    def __init__(self, src, method, key, next_key=None, remove_key=None, dst=None):
        self.load(method, key, next_key, remove_key)
        super().__init__(src, self.to_cg_str(), dst)

    def load(self, method, key=None, next_key=None, remove_key=None) -> None:
        self.method = method
        self.key = key
        self.next_key = next_key
        self.remove_key = remove_key

    def place(self, key):
        self.method = "PLACE"
        self.key = key
        return self

    def get_remove(self, keys):
        ret = []
        for key in keys:
            ret.append(Action(self.method + "&TAKE", self.key, self.next_key, key))
        return ret

    def move(self, key1, key2):
        self.key = key1
        self.next_key = key2
        self.method = "MOVE"
        return self

    def load(self, s: str):
        self.method, self.key, *args = s.split(";")
        if len(args) == 1:
            if self.method == "PLACE&TAKE":
                self.remove_key = args[0]
            else:
                self.next_key = args[0]
        elif len(args) == 2:
            self.next_key, self.remove_key = args
        else:
            self.remove_key = None
        return self

    def to_cg_str(self) -> str:
        ret = [self.method, self.key]
        if self.next_key:
            ret.append(self.next_key)
        if self.remove_key:
            ret.append(self.remove_key)
        return ";".join(ret)
