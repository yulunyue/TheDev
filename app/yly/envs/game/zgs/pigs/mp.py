from .base import Pig
from ..card.export import Tao, Sha, Nzrq, Wjqf, Juedou, Wxkj, Shan, CardBase


class Mp(Pig):
    state = Pig.IS_GOOD

    def power_change(self, num, c: CardBase):
        super().power_change(num, c)
        if num < 0:
            if c.owner.state == self.UN_KNOWN:
                c.owner.state = self.LIKE_BAD

    def is_enemy(self, c: "Pig"):
        return c.state in {self.IS_BAD, self.LIKE_BAD}

    def is_firend(self, c):
        return c.state == self.IS_GOOD
