from .base import CardBase


class Nzrq(CardBase):
    type = "N"
    title = "南"
    can_use = True

    def do(self):
        dst = self.owner.next
        from ..util import wx, Pig

        self.use()
        while dst != self.owner:
            if not wx(self.owner, dst, Pig.IS_BAD, self):
                dst.hander(self)
            dst = dst.next
