from .base import CardBase


class Nzrq(CardBase):
    type = "N"
    title = "南"
    can_use = True

    def do(self, f=None):
        dst = self.owner.next
        from ..util import wx, Pig

        while dst != self.owner:
            if not wx(self.owner, dst, Pig.IS_BAD):
                dst.hander(self)
            dst = dst.next
        self.use()
