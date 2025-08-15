from typing import List
from common.algo.export import sin, cos


class Data:
    def __init__(self):
        self.speed_x = self.speed_y = 0
        self.add_speed_x = self.add_speed_y = 0

    def set_history(self, history):
        self.history: List[Data] = history
        return self

    def set_data(
        self,
        x,
        y,
        next_checkpoint_x,
        next_checkpoint_y,
        next_checkpoint_dist,
        next_checkpoint_angle,
        power,
        inputs=None,
    ):
        self.x = x
        self.y = y
        self.next_checkpoint_x = next_checkpoint_x
        self.next_checkpoint_y = next_checkpoint_y
        self.next_checkpoint_dist = next_checkpoint_dist
        self.next_checkpoint_angle = next_checkpoint_angle
        self.power = power
        if self.history:
            self.speed_x = self.x - self.history[-1].x
            self.speed_y = self.y - self.history[-1].y
            self.add_speed_x = self.speed_x - self.history[-1].speed_x
            self.add_speed_y = self.speed_y - self.history[-1].speed_y
        self.history.append(self)
        return self

    def dump(self):
        return dict(
            # x=self.x,
            dx=self.next_checkpoint_x - self.x,
            sx=self.speed_x,
            ax=self.add_speed_x,
            # y=self.y,
            # ny=self.next_checkpoint_y,
            # sy=self.speed_y,
            # ay=self.add_speed_y,
            # p=self.power,
            # py=self.power * sin(self.next_checkpoint_angle),
            # px=self.power * cos(self.next_checkpoint_angle),
        )
