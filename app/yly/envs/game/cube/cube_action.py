from common.algo.export import State, encode_data, decode_data, Action
from .constant import C


class CubeAction(Action):
    def __init__(self, src, action, dst=None):
        super().__init__(src, action, dst)
        self.axis, self.layer_id, self.rotate = self.action
        
    def show(self, msg=None):
        axis_names = ["y", "x", "z"]
        rotate_names = {-1: "逆时针90°", 1: "顺时针90°", 2: "180°"}
        return f"{axis_names[self.axis]}轴 第{self.layer_id}层 {rotate_names[self.rotate]}旋转"
