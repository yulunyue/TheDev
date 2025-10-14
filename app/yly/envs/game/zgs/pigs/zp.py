from .base import Pig
from .mp import Mp


class Zp(Pig):
    def is_enemy(self, c):
        if c.state == self.IS_BAD:
            self.state = self.IS_GOOD
            return True
        return False

    def is_firend(self, c):
        if c.state == self.IS_GOOD:
            self.state = self.IS_GOOD
            return True
        return False

    def power_change(self, num, c):
        super().power_change(num, c)
        if self.power == 0 and isinstance(c.owner, Mp):
            c.owner.lose_all_card()
