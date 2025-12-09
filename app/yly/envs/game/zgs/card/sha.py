from .base import CardBase


class Sha(CardBase):
    type = "K"
    title = "杀"

    def do(self, f=None):
        if self.owner.use_sha and not self.owner.haz_zg():
            return
        if self.owner.is_enemy(self.owner.next):
            self.set_dst(self.owner.next)
            self.use(f)

    def hander(self):  # 使用中再处理
        if self.dst:
            self.owner.use_sha = True
            self.dst.hander(self)
