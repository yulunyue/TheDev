from .base import CardBase, logger


class Juedou(CardBase):
    type = "F"
    title = "决"

    def do(self):
        from ..util import wx, Fp

        aim = None
        if self.owner.__class__ == Fp:
            aim = logger.mp
            self.owner.is_enemy(aim)
        else:
            cur = self.owner.next
            while cur != self.owner:
                if self.owner.is_enemy(cur):
                    aim = cur
                    break
                cur = cur.next
        if aim is not None:
            self.use()
            if not wx(self.owner, aim, self.owner.IS_BAD, self):
                aim.hander(self)
