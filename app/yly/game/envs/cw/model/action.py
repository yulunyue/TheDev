from app.yly.game.envs.cw.model.shape import ShapeBase, C
from .constant import VE
from common.algo.search.state import Action


class CwAction(Action):

    def __init__(self, src, f, method, t, dst: ShapeBase):
        super().__init__(src, "", dst)
        self.f: ShapeBase = f
        self.t: ShapeBase = t
        self.method = method
        self.aim = None
        self.reward = self.get_reward()
        self.action = " ".join(self.ans)

    def get_reward(self):
        self.ans = [str(self.f.unit_id), self.method]
        if self.method == C.ACTION_MOVE:
            self.ans.extend([str(self.t.x), str(self.t.y)])
            if self.f.unit_type == C.TYPE_CULT_LEADER:
                self.aim = self.t.path.get_near(1 - self.f.owner)
                if self.aim:
                    if self.t.get_dis(self.aim) == C.VALUE_DAMAGE_MAX - 1:
                        return [VE.LEADER_IN_OP_CULT_RANGE]
                    # fv = self.f.get_dis(self.aim)
                    # if fv <= self.t.get_dis(self.aim) and fv <= C.VALUE_DAMAGE_MAX:
                    #     return [VE.LEADER_AVOID_OP_CULT]
                self.aim = self.t.path.get_near(2)
                if self.aim:
                    return [VE.LEADER_NEAR_NEUTRAL_CULT, -self.t.get_dis(self.aim)]
            elif self.f.unit_type == C.TYPE_CULTIST:
                self.aim = self.t.path.leaders[1 - self.f.owner]
                if self.aim:
                    return [VE.CULT_NEAR_OP_LEADER, -self.t.get_dis(self.aim)]
                return [VE.NULL_STATE]
        elif self.method == C.ACTION_SHOOT:
            self.ans.extend([str(self.t.unit_id)])
            if self.f.get_dis(self.t) < C.VALUE_DAMAGE_MAX:
                if self.t.unit_type == C.TYPE_CULT_LEADER:
                    return [VE.CULT_SHOOT_OP_LEADER, -self.f.get_dis(self.t)]
                if self.t.unit_type == C.TYPE_CULTIST:
                    return [VE.CULT_SHOOT_OP_CULT, -self.f.get_dis(self.t)]
        elif self.method == C.ACTION_CONVERT:
            self.ans.extend([str(self.t.unit_id)])
            return [VE.LEADER_INFECT_NEUTRAL_CULT]
        self.ans = [C.ACTION_WAIT]
        return [VE.WAIT_STATE]

    def __repr__(self):
        action = self.action
        if self.method == C.ACTION_MOVE:
            k = self.t.y - self.f.y, self.t.x - self.f.x
            # print(self.f, self.t)
            action = {(0, 1): "RIGHT", (0, -1): "LEFT", (1, 0): "DOWN", (-1, 0): "UP"}[
                k
            ]
        return f"src:{self.f}; action:{action}; aim:{self.aim}; reward:{VE.to_str(self.reward[0])}; args:{self.reward[1:]};"
