from .base import CardBase


class Zgll(CardBase):
    type = "Z"
    title = "诸"

    def do(self, f=None):
        self.owner._has_zg = True
        return super().do(f)
