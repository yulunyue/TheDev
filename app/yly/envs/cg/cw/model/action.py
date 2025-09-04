from app.yly.envs.cg.cw.shape.cell import ShapeBase, C
from common.algo.search.state import State, Action
from .state import CwState
import copy


class CwAction(Action):
    src: CwState

    def __init__(self, src, f: ShapeBase, method, t: ShapeBase, param0=None):
        self.f_id, self.f_x, self.f_y = f.unit_id, f.x, f.y
        self.t_id, self.t_x, self.t_y = t.unit_id, t.x, t.y
        self.method = method
        self.param0 = param0
        self.owner = f.owner
        super().__init__(src, self.get_action_str())

    def get_action_str(self):
        ans = [str(self.f_id), self.method]
        if self.method == C.ACTION_MOVE:
            ans.extend([str(self.t_x), str(self.t_y)])
        else:
            ans.extend([str(self.t_id)])
        return " ".join(ans)

    def show(self):
        ans = [f"{self.f_id} {self.method}"]
        if self.method == C.ACTION_MOVE:
            k = self.t_y - self.f_y, self.t_x - self.f_x
            action = {(0, 1): "RIGHT", (0, -1): "LEFT", (1, 0): "DOWN", (-1, 0): "UP"}[
                k
            ]
            ans[0] += f" {action}"
        else:
            ans[0] += f" {self.t_id}"
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
            dst[self.f_id][C.DATA_POS_y] = self.t_y
            dst[self.f_id][C.DATA_POS_x] = self.t_x
        elif self.method == C.ACTION_CONVERT:
            dst[self.t_id][C.DATA_POS_owner] = self.owner
        else:
            dst[self.t_id][C.DATA_POS_hp] -= self.param0
        self.dst = self.src.__class__.new(
            ",".join([f"{v[0]} {v[1]} {v[2]} {v[3]} {v[4]} {v[5]}" for v in dst])
        )
        return self.dst
