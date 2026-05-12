from common.algo.export import State, encode_data, decode_data, Action
from .constant import C


class CubeAction(Action):
    def set_view(self, c, d, r):
        self.axis, self.layer_id, self.rotate = c, d, r
        self.action = (c, d, r)
        return self

    def show(self, msg=None):
        return ""
