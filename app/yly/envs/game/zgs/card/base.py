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
        logger.debug(f"{self.owner.name} use {self.title}")  # 打牌
        self.hander()  # 响应牌
        self.use_finish()  # 删除牌  三个阶段控制

    def hander(self):
        pass

    def use_finish(self):
        idx = 0
        while idx < len(self.owner.card_map[self.type]):
            d = self.owner.card_map[self.type][idx]
            if d == self:
                break
            idx += 1
        if idx < len(self.owner.card_map[self.type]):
            self.owner.card_map[self.type].pop(idx)
        if self.pre:
            self.pre.next = self.next
        else:
            self.owner.head = self.next
        if self.next:
            self.next.pre = self.pre
        else:
            self.owner.tail = self.pre
        return self

    def do(self, f: "CardBase" = None):
        self.use(f)
