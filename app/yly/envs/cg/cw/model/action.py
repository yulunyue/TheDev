from app.yly.envs.cg.cw.shape.cell import ShapeBase, C
from common.algo.search.state import State, Action
from .state import CwState, ENV
from common.util.export import logger, copy


class CwAction(Action):
    src: CwState

    def __init__(self, src, f: ShapeBase, method, t: ShapeBase, param0=None):
        self.fid = f.unit_id  # 由于shape会移动，所以不能存实例，得存id
        self.tx = t.x
        self.ty = t.y
        self.fx = f.x
        self.fy = f.y
        self.tid = t.unit_id
        self.method = method
        self.param0 = param0
        self.owner = f.owner
        self.reward = 0
        super().__init__(src, self.get_action_str(f, t))

    def get_action_str(self, f: ShapeBase, t: ShapeBase):
        ans = [str(self.fid), self.method]
        self.show_msg = f"{f.k} {f.view()} {self.method}"
        if self.method == C.ACTION_MOVE:
            k = self.ty - f.y, self.tx - f.x
            self.show_msg += f" {C.DR_VIEW[k]}"
            ans.extend([str(self.tx), str(self.ty)])
        else:
            self.show_msg += f" {t.k} {t.view()} {self.param0}"
            ans.extend([str(self.tid)])
        return " ".join(ans)

    def show(self):
        return self.show_msg

    def get_dst(self):
        if self.action == C.ACTION_WAIT:
            return self
        if self.dst:
            return self.dst

        # ENV.load_shapes(self.src.board)
        dst = copy.deepcopy(self.src.board)
        # logger.map(id=id(self), unit_id=self.f.unit_id, y=self.f.y, x=self.f.x)
        if self.method == C.ACTION_MOVE:
            dst[self.fid][C.DATA_POS_y] = self.ty
            dst[self.fid][C.DATA_POS_x] = self.tx
        elif self.method == C.ACTION_CONVERT:
            dst[self.tid][C.DATA_POS_owner] = self.owner
        elif self.method == C.ACTION_SHOOT:
            dst[self.tid][C.DATA_POS_hp] -= self.param0
        self.dst = CwState.new(
            ",".join([f"{v[0]} {v[1]} {v[2]} {v[3]} {v[4]} {v[5]}" for v in dst])
        ).set_player_id(1 - self.owner)
        return self.dst
