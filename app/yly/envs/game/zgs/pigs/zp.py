from .base import Pig
from .mp import Mp


class Zp(Pig):
    def is_enemy(self, c):
        return c.state == self.IS_BAD

    def is_firend(self, c):
        return c.state == self.IS_GOOD

    def power_change(self, num, c):
        super().power_change(num, c)
        if self.power == 0 and isinstance(c.owner, Mp):
            c.owner.lose_all_card()
