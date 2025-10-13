from .base import Pig


class Fp(Pig):
    def is_enemy(self, c):
        return c.state == self.IS_GOOD

    def is_firend(self, c):
        return c.state == self.IS_BAD

    def power_change(self, num, c):
        super().power_change(num, c)
        if self.power == 0:
            c.owner.get_num_card(3)
