from .base import CardBase, logger


class Nzrq(CardBase):
    type = "N"
    title = "南"

    def do(self):
        dst = self.owner.next
        from ..util import wx, Pig

        self.use()
        while dst != self.owner and not logger.game_over():
            if not wx(self.owner, dst, Pig.IS_BAD, self):
                dst.hander(self)
            dst = dst.next
