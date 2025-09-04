from app.yly.envs.cg.cw.shape.cell import ShapeBase, C
from common.algo.search.state import State, Action
from .state import CwState
import copy


class CwAction(Action):
    src: CwState

    def __init__(self, src, f: ShapeBase, method, t, param0=None):
        self.f: ShapeBase = f
        self.t: ShapeBase = t
        self.method = method
        self.param0 = param0
        super().__init__(src, self.get_action_str())

    def get_action_str(self):
        ans = [str(self.f.unit_id), self.method]
        if self.method == C.ACTION_MOVE:
            ans.extend([str(self.t.x), str(self.t.y)])
        else:
            ans.extend([str(self.t.unit_id)])
        return " ".join(ans)

    def show(self):
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
        ans += [f"  reward:{self.get_dst().get_reward()}"]
        return "\n".join(ans)

    def get_dst(self):
        if self.action == C.ACTION_WAIT:
            return self
        if self.dst:
            return self.dst
        from .state import CwState

        dst = copy.deepcopy(self.src.board)
        if self.method == C.ACTION_MOVE:
            dst[self.f.unit_id - 1][C.DATA_POS_y] = self.t.y
            dst[self.f.unit_id - 1][C.DATA_POS_x] = self.t.x
        elif self.method == C.ACTION_CONVERT:
            dst[self.t.unit_id - 1][C.DATA_POS_owner] = self.f.owner
        else:
            dst[self.t.unit_id - 1][C.DATA_POS_hp] -= self.param0
        self.dst = CwState.new(
            ",".join([f"{v[0]} {v[1]} {v[2]} {v[3]} {v[4]} {v[5]}" for v in dst])
        )
        return self.dst
