from common.mock import MockCg
from app.yly.game.envs.mpr.constant import C


class AiMode:
    TESTX = "TESTX"
    POWER_100 = "POWER_100"


class Ai:
    MODE = "MOCK_MODE"

    def __init__(self):
        self.speed_x = None
        self.last_x = None
        self.last_y = None
        self.speed_y = None
        self.pi = 0.1

    def execute(
        self,
        x,
        y,
        next_checkpoint_x,
        next_checkpoint_y,
        next_checkpoint_dist,
        next_checkpoint_angle,
        *args,
        **kw,
    ):
        if self.last_x is None:
            self.last_x, self.last_y = x, y
            return next_checkpoint_x, next_checkpoint_y, 100
        self.speed_x = x - self.last_x
        self.speed_y = y - self.last_y
        self.e_t = next_checkpoint_dist
        power = self.get_power()
        self.last_x, self.last_y = x, y
        return next_checkpoint_x, next_checkpoint_y, min(int(power), 100)

    def get_power(self):
        if self.MODE == AiMode.POWER_100:
            return 100
        return self.pi * self.e_t

    def get_info(self):  # -> dict[str, Any]:
        return dict(
            speed_x=self.speed_x,
            speed_y=self.speed_y,
            last_x=self.last_x,
            last_y=self.last_y,
        )


class Mpr(MockCg):
    game_id = "595803248f16a6655bc56f0b970000a821ea4db0"
    agents_ids = [-1, -2]
    name = "mpr"

    def main(self):
        ai = Ai()
        while True:
            (
                x,
                y,
                next_checkpoint_x,
                next_checkpoint_y,
                next_checkpoint_dist,
                next_checkpoint_angle,
            ) = self.ii()
            opponent_x, opponent_y = self.ii()
            dst_x, dst_y, power = ai.execute(
                x,
                y,
                next_checkpoint_x,
                next_checkpoint_y,
                next_checkpoint_dist,
                next_checkpoint_angle,
                opponent_x,
                opponent_y,
            )
            self.log(
                x=x,
                y=y,
                dst_x=dst_x,
                dst_y=dst_y,
                next_x=next_checkpoint_x,
                next_y=next_checkpoint_y,
                next_ang=next_checkpoint_angle,
                dist=next_checkpoint_dist,
                opponent_x=opponent_x,
                opponent_y=opponent_y,
                power=power,
                **ai.get_info(),
            )
            self.output(f"{dst_x} {dst_y} {power}")


if __name__ == "__main__":
    Mpr().main()
