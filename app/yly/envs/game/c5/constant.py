class Constant:
    def load(self, in_row=4, width=6, height=6):
        self.in_row = in_row
        self.width = width
        self.height = height
        self.size = self.width * self.height
        self.init_mask = 0
        return self

    def init_lines(self):
        self.lines = []
        for i in range(self.size):
            y, x = i // self.size.i % self.size


C = Constant().load()
