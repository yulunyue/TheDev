from .base import Pig
from ..log import logger


class Fp(Pig):
    def is_enemy(self, c):
        if c.state == self.IS_GOOD:
            self.state = self.IS_BAD
            return True
        return False

    def is_firend(self, c):
        if c.state == self.IS_BAD:
            self.state = self.IS_BAD
            return True
        return False

    def power_change(self, num, c):
        super().power_change(num, c)
        if self.power == 0:
            logger.fz_num_change(-1)
            if not logger.game_over():
                c.owner.get_num_card(3, c.owner.head is None)
