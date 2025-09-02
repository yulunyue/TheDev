from app.yly.envs.cg.cw.model.shape import ShapeBase, C
from .constant import VE


class CwAction:

    def __init__(self, f: ShapeBase, method, t):
        self.f: ShapeBase = f
        self.t: ShapeBase = t
        self.method = method

    @property
    def action(self):
        ans = [str(self.f.unit_id), self.method]
        if self.method == C.ACTION_MOVE:
            ans.extend([str(self.t.x), str(self.t.y)])
        else:
            ans.extend([str(self.t.unit_id)])
        return " ".join(ans)

    def __repr__(self):
        ans = f"{self.f.view()} {self.method}"
        if self.method == C.ACTION_MOVE:
            k = self.t.y - self.f.y, self.t.x - self.f.x
            # print(self.f, self.t)
            action = {(0, 1): "RIGHT", (0, -1): "LEFT", (1, 0): "DOWN", (-1, 0): "UP"}[
                k
            ]
            ans += f" {action}"
        else:
            ans += f" {self.t.view()}"
        return ans
