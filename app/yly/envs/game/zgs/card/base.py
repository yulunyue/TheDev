from common.util.export import List
from ..log import logger


class CardBase:
    type: str
    is_use = False
    title = ""
    pre: "CardBase" = None
    next: "CardBase" = None
    dst = None

    def set_dst(self, dst):
        from ..pigs.base import Pig

        self.dst: Pig = dst
        return self

    def set_owner(self, owner):
        from ..pigs.base import Pig

        self.owner: Pig = owner

    def use(self, f: "CardBase" = None):
        s = ""
        if self.dst:
            s = f"to {self.dst.name}"
        if f:
            s = f"for {f.owner.name} use {f.title}"
        # logger.debug(f"{self.owner.name} use {self.title} {s}")
        self.pre.next = self.next
        if self.next:
            self.next.pre = self.pre
        else:
            self.owner.tail = self.pre
        return self

    def do(self, f: "CardBase" = None):
        self.use(f)
