from app.yly.game.envs.cw.model.shape import ShapeBase, C
from .constant import VE


class Action:
    def __init__(self, g, src: ShapeBase, dst: ShapeBase):
        from app.yly.game.envs.cw.model.world import World

        self.g: World = g
        self.src: ShapeBase = src
        self.dst: ShapeBase = dst

    def calc(self):
        if self.src.unit_type == C.TYPE_CULTIST:
            return self.calc_cultist()
        return self.calc_cult_leader()

    def calc_cultist(self):
        path = self.g.path_info[self.dst.k]
        if path.op_leader is not None:
            if self.get_shoot_dis(path.op_leader) > 0:
                return [VE.CULT_SHOOT_OP_LEADER]
            elif 1:
                return [VE.CULT_NEAR_OP_LEADER, -self.dst.get_dis(path.op_leader)]
        if path.op_shapes:
            s = path.op_shapes[0]
            if self.get_shoot_dis(s) > 3:
                return [VE.CULT_SHOOT_OP_CULT]
        return [VE.NULL_STATE]

    def get_shoot_dis(self, s: ShapeBase):
        dis_shot = self.dst.get_dis(s)
        damage = C.VALUE_DAMAGE_MAX - dis_shot
        return damage

    def calc_cult_leader(self):
        if self.dst.unit_type == C.TYPE_CULTIST:
            return [VE.LEADER_INFECT_NEUTRAL_CULT]
        path = self.g.path_info[self.dst.k]
        if path.op_shapes:
            op_min_shape = path.op_shapes[0]
            shoot_dis = self.get_shoot_dis(op_min_shape)
            if shoot_dis > 0:
                return [VE.LEADER_AVOID_OP_CULT, shoot_dis]
        if path.neutral_shapes:
            return [VE.LEADER_NEAR_SELF_CULT, -self.dst.get_dis(path.neutral_shapes[0])]
        return [VE.NULL_STATE]

    def get_action(self):
        ans = [str(self.src.unit_id)]
        if self.dst.unit_type == C.TYPE_NULL:
            ans.extend([C.ACTION_MOVE, str(self.dst.x), str(self.dst.y)])
        elif self.dst.unit_type == C.TYPE_CULT_LEADER:
            ans.extend([C.ACTION_SHOOT, str(self.dst.unit_id)])
        else:
            ans.extend([C.ACTION_CONVERT, str(self.dst.unit_id)])
        return " ".join(ans)
