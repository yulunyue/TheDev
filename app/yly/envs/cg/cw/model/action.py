from app.yly.envs.cg.cw.model.shape import ShapeBase, C
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
                self.aim = self.f.path.get_near(1 - self.f.owner)
                aim2 = self.f.path.get_near(2)
                aim2_dis = float("inf")
                if aim2:
                    aim2_dis = aim2.get_dis(self.t)
                if self.aim:
                    aimf = self.aim.get_shoot(self.f)
                    aimt = self.aim.get_shoot(self.t)
                    if aimf and aimf.unit_id == self.f.unit_id:
                        if aimt and aimt.unit_id != self.t.unit_id:
                            return [VE.LEADER_OUT_OP_CULT_RANGE, -aim2_dis]
                        if self.t.get_abs_dis(self.aim) > self.f.get_abs_dis(self.aim):
                            return [VE.LEADER_AWAY_OP_CULT_RANGE, -aim2_dis]
                    if aimt and aimt.unit_id == self.t.unit_id:
                        return [VE.LEADER_IN_OP_CULT_RANGE]
                self.aim = aim2
                return [VE.LEADER_NEAR_NEUTRAL_CULT, -aim2_dis]
            elif self.f.unit_type == C.TYPE_CULTIST:
                self.aim = self.f.path.leaders[1 - self.f.owner]
                if self.aim:
                    return [VE.CULT_NEAR_OP_LEADER, -self.aim.get_dis(self.t)]
                return [VE.NULL_STATE]
        elif self.method == C.ACTION_SHOOT:
            self.ans.extend([str(self.t.unit_id)])
            self.aim = self.f.get_shoot(self.t)
            if self.aim and self.aim.unit_id == self.t.unit_id:
                if self.t.unit_type == C.TYPE_CULT_LEADER:
                    return [VE.CULT_SHOOT_OP_LEADER, -self.f.get_abs_dis(self.t)]
                if self.t.unit_type == C.TYPE_CULTIST:
                    return [VE.CULT_SHOOT_OP_CULT, -self.f.get_abs_dis(self.t)]
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
