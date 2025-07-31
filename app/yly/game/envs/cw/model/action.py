from app.yly.game.envs.cw.model.shape import ShapeBase, C
from .constant import VE
from common.algo.search.state import Action


class CwAction(Action):

    def __init__(self, src, f, method, t, dst: ShapeBase):
        super().__init__(src, "", dst)
        self.f: ShapeBase = f
        self.t: ShapeBase = t
        self.method = method
        self.reward = self.get_reward()
        self.action = " ".join(self.ans)

    def get_reward(self):
        self.ans = [str(self.f.unit_id), self.method]
        if self.method == C.ACTION_MOVE:
            self.ans.extend([str(self.t.x), str(self.t.y)])
            if self.f.unit_type == C.TYPE_CULT_LEADER:
                near = self.t.path.get_near(1 - self.f.owner)
                if near and self.t.get_dis(near) <= C.VALUE_DAMAGE_MAX:
                    return [VE.LEADER_IN_OP_CULT_RANGE]
                near = self.t.path.get_near(2)
                if near:
                    return [VE.LEADER_NEAR_NEUTRAL_CULT, self.t.get_dis(near)]
            elif self.f.unit_type == C.TYPE_CULTIST:
                op_leader = self.t.path.leaders[1 - self.f.owner]
                if op_leader:
                    return [VE.CULT_NEAR_OP_LEADER, self.t.get_dis(op_leader)]
        elif self.method == C.ACTION_SHOOT:
            self.ans.extend([str(self.t.unit_id)])
            if self.t.owner == 2:
                return
            if self.f.get_dis(self.t) >= C.VALUE_DAMAGE_MAX:
                return
            if self.t.unit_type == C.TYPE_CULT_LEADER:
                return [VE.CULT_SHOOT_OP_LEADER, -self.f.get_dis(self.t)]
            if self.t.unit_type == C.TYPE_CULTIST:
                return [VE.CULT_SHOOT_OP_CULT, -self.f.get_dis(self.t)]
        elif self.method == C.ACTION_CONVERT:
            return [VE.LEADER_INFECT_NEUTRAL_CULT]
        else:
            self.ans = [C.ACTION_WAIT]
            return [VE.NULL_STATE]
