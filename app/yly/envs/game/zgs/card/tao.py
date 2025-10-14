from .base import CardBase


class Tao(CardBase):
    type = "P"
    title = "桃"

    def do(self, p: CardBase = None):
        if self.owner.power < 4:
            self.use(p)
            self.owner.power_change(1, self)
