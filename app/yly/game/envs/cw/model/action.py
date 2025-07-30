from app.yly.game.envs.cw.model.shape import ShapeBase, C
from .constant import VE


class Action:
    def __init__(self, g, src: ShapeBase, dst: ShapeBase):
        from app.yly.game.envs.cw.model.world import World

        self.g: World = g
        self.src: ShapeBase = src
        self.dst: ShapeBase = dst

    def calc(self):
        dst = self.dst
        if self.src.unit_type == C.TYPE_CULTIST:
            ret, dst = self.calc_cultist()
        else:
            ret = self.calc_cult_leader()
        return ret, self.get_action(dst)

    def calc_cultist(self):
        path = self.g.path_info[self.dst.k]
        if self.dst.unit_type != C.TYPE_NULL:
            return [VE.NULL_STATE], None
        if path.op_leader is not None:
            if self.get_shoot_dis(path.op_leader) > 0:
                return [VE.CULT_SHOOT_OP_LEADER], path.op_leader
            else:
                return [
                    VE.CULT_NEAR_OP_LEADER,
                    -self.dst.get_dis(path.op_leader),
                ], self.dst
        if path.op_shapes:
            s = path.op_shapes[0]
            if self.get_shoot_dis(s) > 3:
                return [VE.CULT_SHOOT_OP_CULT], s
        return [VE.NULL_STATE], None

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
                return [VE.LEADER_AVOID_OP_CULT, -shoot_dis]
        if path.neutral_shapes:
            return [
                VE.LEADER_NEAR_NEUTRAL_CULT,
                -self.dst.get_dis(path.neutral_shapes[0]),
            ]
        return [VE.NULL_STATE]

    def get_action(self, dst: "ShapeBase"):
        ans = [str(self.src.unit_id)]
        if dst is None:
            ans = [C.ACTION_WAIT]
        elif dst.unit_type == C.TYPE_NULL:
            ans.extend([C.ACTION_MOVE, str(dst.x), str(dst.y)])
        elif (
            self.src.unit_type == C.TYPE_CULT_LEADER and dst.unit_type == C.TYPE_CULTIST
        ):
            ans.extend([C.ACTION_CONVERT, str(dst.unit_id)])
        elif self.src.unit_type == C.TYPE_CULTIST:
            ans.extend([C.ACTION_SHOOT, str(dst.unit_id)])
        else:
            raise Exception(self.src, self.dst)
        return " ".join(ans)
