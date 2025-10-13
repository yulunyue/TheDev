from .base import CardBase


class Tao(CardBase):
    type = "P"
    title = "桃"
    can_use = True

    def do(self, p: CardBase = None):
        if self.owner.power < 4:
            self.use(p)
            self.owner.power += 1
