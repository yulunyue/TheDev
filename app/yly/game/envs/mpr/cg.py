from common.mock import MockCg
from app.yly.game.envs.mpr.constant import C
from .model.algo import MprAlgo


class Mpr(MockCg):
    game_id = "595803248f16a6655bc56f0b970000a821ea4db0"
    agents_ids = [-1, -2]
    name = "mpr"

    def main(self):
        ai = MprAlgo()
        while True:
            (
                x,
                y,
                next_checkpoint_x,
                next_checkpoint_y,
                next_checkpoint_dist,
                next_checkpoint_angle,
            ) = self.ii()
            ai.set_op_pos(self.ii())
            dst_x, dst_y, power = ai.execute(
                x=x,
                y=y,
                next_checkpoint_x=next_checkpoint_x,
                next_checkpoint_y=next_checkpoint_y,
                next_checkpoint_dist=next_checkpoint_dist,
                next_checkpoint_angle=next_checkpoint_angle,
            )
            self.log(**ai.get_param())
            self.output(f"{dst_x} {dst_y} {power}")


if __name__ == "__main__":
    Mpr().main()
