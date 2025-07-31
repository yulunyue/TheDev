from app.yly.game.envs.cw.model.shape import ShapeBase, C
from .constant import VE
from common.algo.search.state import Action


class CwAction(Action):

    def __init__(self, src, f, method, t, dst: ShapeBase):
        super().__init__(src, "", dst)
        self.f: ShapeBase = f
        self.t: ShapeBase = t
        self.method = method
        self.action = self.get_action_str()

    def calc(self):
        if self.f.unit_type == C.TYPE_CULTIST:
            ret, dst = self.calc_cultist()
        else:
            ret = self.calc_cult_leader()
        return self

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

    def get_action_str(self):
        ans = [str(self.f.unit_id), self.method]
        if self.method == C.ACTION_MOVE:
            ans.extend([str(self.t.x), str(self.t.y)])
        else:
            ans.extend([str(self.t.unit_id)])
        return " ".join(ans)
