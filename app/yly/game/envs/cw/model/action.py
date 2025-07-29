from app.yly.game.envs.cw.model.shape import ShapeBase, C


class Action:
    def __init__(self, g, src: ShapeBase, dst: ShapeBase):
        from app.yly.game.envs.cw.model.world import World

        self.g: World = g
        self.src: ShapeBase = src
        self.dst: ShapeBase = dst

    def calc(self):
        self.score = None
        if self.src.unit_type == C.TYPE_CULTIST:
            self.calc_cultist()
        else:
            self.calc_cult_leader()
        return self

    def calc_cultist(self):
        pass

    def calc_cult_leader(self):
        for node in self.g.cultists[2]:
            self.score = [self.dst]

    def get_action(self):
        ans = [str(self.src.unit_id)]
        if self.dst.unit_type == C.TYPE_NULL:
            ans.extend([C.ACTION_MOVE, str(self.dst.x), str(self.dst.y)])
        elif self.dst.unit_type == C.TYPE_CULT_LEADER:
            ans.extend([C.ACTION_SHOOT, str(self.dst.unit_id)])
        else:
            ans.extend([C.ACTION_CONVERT, str(self.dst.unit_id)])
        return " ".join(ans)
