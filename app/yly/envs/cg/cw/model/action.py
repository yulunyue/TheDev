from app.yly.envs.cg.cw.shape.cell import ShapeBase, C
from .constant import VE


class CwAction:

    def __init__(self, f: ShapeBase, method, t):
        self.f: ShapeBase = f
        self.t: ShapeBase = t
        self.method = method
        self.msgs = []
        self.reward = 0
        self.load()

    def add_reward(self, msg, reward):
        self.reward += reward
        self.msgs.append(f"  {msg}->{reward}")

    def load(self):
        if self.f.unit_type == C.TYPE_CULT_LEADER:
            if self.method == C.ACTION_CONVERT:
                self.add_reward(f"{C.ACTION_CONVERT} {self.t.view()}", 1)
            else:
                self.load_leader_shoot_risk()

    def load_leader_shoot_risk(self):
        for node in self.t.get_path().shapes[1 - self.f.owner]:
            dis = node.can_shoot(self.t)
            if dis > 0:
                self.add_reward(f"SHOOT_BY {node.view()} {dis}", -dis)
            if dis == -1:
                break

    @property
    def action(self):
        ans = [str(self.f.unit_id), self.method]
        if self.method == C.ACTION_MOVE:
            ans.extend([str(self.t.x), str(self.t.y)])
        else:
            ans.extend([str(self.t.unit_id)])
        return " ".join(ans)

    def __repr__(self):
        ans = [f"{self.f.view()} {self.method}"]
        if self.method == C.ACTION_MOVE:
            k = self.t.y - self.f.y, self.t.x - self.f.x
            # print(self.f, self.t)
            action = {(0, 1): "RIGHT", (0, -1): "LEFT", (1, 0): "DOWN", (-1, 0): "UP"}[
                k
            ]
            ans[0] += f" {action}"
        else:
            ans[0] += f" {self.t.view()}"
        ans += self.msgs
        return "\n".join(ans)
