from common.tool.export import Draw
from common.util.export import List, ii, defaultdict
from app.yly.game.envs.mpr.cg import Mpr, C
from common.third_util.export import CGFrames
from common.algo.export import sin, cos


class Util:
    def show(self, freams: List[CGFrames], mode):
        datas = defaultdict(list)
        opponent_x = opponent_y = x = y = None
        last_spped_x = last_spped_y = speed_x = speed_y = None
        last_x = last_y = None
        speed_addx = speed_addy = None
        for f in freams:
            if f.stderr:
                x, y, dst_x, dst_y, dist, opponent_x, opponent_y, power, next_ang = (
                    f.stderr["x"],
                    f.stderr["y"],
                    f.stderr["dst_x"],
                    f.stderr["dst_y"],
                    f.stderr["dist"],
                    f.stderr["opponent_x"],
                    f.stderr["opponent_y"],
                    f.stderr["power"],
                    f.stderr["next_ang"],
                )
                power_x, power_y = power * sin(next_ang), power * cos(next_ang)

                if last_x is not None:
                    speed_x, speed_y = x - last_x, y - last_y
                if last_spped_x is not None:
                    speed_addx, speed_addy = (
                        speed_x - last_spped_x,
                        speed_y - last_spped_y,
                    )
                last_spped_x, last_spped_y = speed_x, speed_y
                last_x, last_y = x, y
                if speed_addx is not None:
                    datas["self_speed_addx"].append(
                        dict(speed_addx=speed_addx, power=power_x)
                    )
                    datas["self_speed_addy"].append(
                        dict(speed_addy=speed_addy, power=power_y)
                    )
                datas["self_x"].append(dict(x=dst_x - x, power=power_x))
                datas["self_y"].append(dict(y=dst_y - y, power=power_y))
                datas["self_d"].append(dict(dist=dist, powwer=power))

            else:
                op_dst_x, op_dst_y, op_power = ii(f.stdout)
                if opponent_x is None:
                    continue
                dist = (
                    (op_dst_x - opponent_x) ** 2 + (op_dst_y - opponent_y) ** 2
                ) ** 0.5
                datas["op"].append(
                    dict(
                        x=opponent_x,
                        y=opponent_y,
                        power=op_power,
                        dst_x=op_dst_x,
                        dst_y=op_dst_y,
                        dist=dist,
                    )
                )
        for k, v in datas.items():
            Draw().draw_lines(v).save(f"{C.SAVE_DIR}/draw/{mode}/{k}.svg")
