from common.algo.export import State, encode_data, decode_data, Action
from .constant import C


class CubeAction(Action):
    def set_view(self, c, d, r):
        self.color, self.layer_id, self.rotate = c, d, r
        self.action = (c, d, r)
        return self

    def show(self, msg=None):

        return super().show(
            f"第{self.layer_id}层{C.COLORS[self.color]}色-顺时针旋转{self.rotate}圈"
        )
