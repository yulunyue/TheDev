from common.util.export import List, Dict, logger
from common.mock import MockCf

O1 = """Case:1
000:00 red iceman 1 born
000:00 blue lion 1 born
000:10 red iceman 1 marched to city 1 with 50 elements and force 50
000:10 blue lion 1 marched to city 2 with 50 elements and force 50
000:30 red iceman 1 earned 10 elements for his headquarter
000:30 blue lion 1 earned 10 elements for his headquarter
000:50 59 elements in red headquarter
000:50 59 elements in blue headquarter
001:00 red lion 2 born
001:00 blue dragon 2 born
001:10 red lion 2 marched to city 1 with 50 elements and force 50
001:10 blue lion 1 marched to city 1 with 50 elements and force 50
001:10 red iceman 1 marched to city 2 with 41 elements and force 70
001:10 blue dragon 2 marched to city 2 with 10 elements and force 20
001:40 red lion 2 attacked blue lion 1 in city 1 with 50 elements and force 50
001:40 blue lion 1 was killed in city 1
001:40 red lion 2 earned 10 elements for his headquarter
001:40 blue dragon 2 attacked red iceman 1 in city 2 with 10 elements and force 20
001:40 red iceman 1 fought back against blue dragon 2 in city 2
001:40 blue dragon 2 was killed in city 2
001:40 red iceman 1 earned 10 elements for his headquarter
001:50 21 elements in red headquarter
001:50 49 elements in blue headquarter
002:00 blue ninja 3 born
002:10 red lion 2 marched to city 2 with 100 elements and force 50
002:10 blue ninja 3 marched to city 2 with 20 elements and force 50
002:10 red iceman 1 reached blue headquarter with 29 elements and force 70
002:40 blue ninja 3 attacked red lion 2 in city 2 with 20 elements and force 50
002:40 red lion 2 fought back against blue ninja 3 in city 2
002:40 blue ninja 3 was killed in city 2
002:40 red lion 2 earned 10 elements for his headquarter
002:40 red flag raised in city 2
002:50 23 elements in red headquarter
002:50 29 elements in blue headquarter
003:10 red lion 2 reached blue headquarter with 58 elements and force 50
003:10 blue headquarter was taken"""
O2 = """Case:2
000:00 red iceman 1 born
000:00 blue lion 1 born
000:10 red iceman 1 marched to city 1 with 20 elements and force 20
000:10 blue lion 1 marched to city 1 with 20 elements and force 20
000:40 red iceman 1 attacked blue lion 1 in city 1 with 20 elements and force 20
000:40 blue lion 1 was killed in city 1
000:40 red iceman 1 earned 10 elements for his headquarter
000:50 22 elements in red headquarter
000:50 20 elements in blue headquarter
001:00 red lion 2 born
001:00 blue dragon 2 born
001:10 red lion 2 marched to city 1 with 20 elements and force 20
001:10 blue dragon 2 marched to city 1 with 20 elements and force 20
001:10 red iceman 1 reached blue headquarter with 39 elements and force 40
001:40 red lion 2 attacked blue dragon 2 in city 1 with 20 elements and force 20
001:40 blue dragon 2 was killed in city 1
001:40 red lion 2 earned 10 elements for his headquarter
001:40 red flag raised in city 1
001:50 12 elements in red headquarter
001:50 0 elements in blue headquarter
002:10 red lion 2 reached blue headquarter with 20 elements and force 20
002:10 blue headquarter was taken"""


class Action:
    def __init__(self, msgs: List[str]):
        self.msgs = msgs

    def __str__(self):
        return " ".join(self.msgs)


LOGS: Dict[int, List[Action]] = dict()


def add_action(a: Action):
    if Solution.now_t not in LOGS:
        LOGS[Solution.now_t] = []
    LOGS[Solution.now_t].append(a)


class Unit:
    attack_power: int = None
    hp: int = None
    type_name = ""
    BORN = "born"
    MARCHED = "marched to"
    earned = "earned"

    def __init__(self, city: "City"):
        self.cmd: Commander = city
        self.city: City = city
        self.key = self.cmd.shape_idx

    def action(self, s, city=None):
        ret = [
            "red" if self.cmd.color == Commander.RED else "blue",
            self.type_name,
            str(self.key),
        ] + [s]
        if s == self.MARCHED:
            ret.extend([str(self.city), self.info()])
            self.city = city
        elif s == self.earned:
            ret.append(f"{self.city.hp} elements for his headquarter")
            self.cmd.hp += self.city.hp
            self.city.hp = 0

        add_action(Action(ret))

    def info(self):
        return f"with {self.hp} and force {self.attack_power}"


class Dragon(Unit):
    type_name = "dragon"


class Ninja(Unit):
    type_name = "ninja"


class IceMan(Unit):
    type_name = "iceman"


class Lion(Unit):
    type_name = "lion"


class Wolf(Unit):
    type_name = "wolf"


SHAPES: List[Unit] = [Dragon, Ninja, IceMan, Lion, Wolf]


class City:
    hp = 0

    def __init__(self, city_idx):
        self.city_idx = city_idx
        self.shape_map: List[Unit] = [None, None]
        self.flag = None

    def __str__(self):
        return f"city {self.city_idx}"


class Commander(City):
    RED = 0
    BLUE = 1

    def __init__(self, color, hp, city_idx):
        self.hp = hp
        self.color = color
        if self.color == Commander.RED:
            self.shape_clss: List[Unit] = [IceMan, Lion, Wolf, Ninja, Dragon]
        else:
            self.shape_clss: List[Unit] = [Lion, Ninja, Dragon, IceMan, Wolf]
        self.shape_idx = 0
        # self.shapes_all: Dict[int, Unit] = {}
        super().__init__(city_idx)


class Solution(MockCf):
    now_t = 0
    uri = "http://bailian.openjudge.cn/practice/3750/"

    def get_cases(self):
        return [
            dict(
                main_hp=99,
                city_num=2,
                t=1000,
                init_hps=[10, 20, 50, 50, 30],
                init_attack_power=[20, 50, 50, 50, 50],
                case_id=1,
                result=O1,
            ),
            # dict(
            #     main_hp=40,
            #     city_num=1,
            #     t=1000,
            #     init_hps=[20, 20, 20, 20, 20],
            #     init_attack_power=[20, 20, 20, 20, 20],
            #     result=O2,
            # ),
        ]

    def execute(self, main_hp, city_num, t, init_hps, init_attack_power, case_id):
        self.cmds = [
            Commander(Commander.RED, main_hp, 0),
            Commander(Commander.BLUE, main_hp, city_num + 1),
        ]

        self.citys = (
            [self.cmds[0]] + [City(i + 1) for i in range(city_num)] + [self.cmds[1]]
        )
        for i, v in enumerate(SHAPES):
            v.attack_power, v.hp = init_attack_power[i], init_hps[i]
        LOGS.clear()
        Solution.now_t = 0
        while Solution.now_t < t:
            tm = Solution.now_t % 60
            if getattr(self, f"do_when_{tm}")():
                break
            Solution.now_t += 10
        ans = [f"Case:{case_id}"]
        for t in sorted(LOGS.keys()):
            k = "%03d:%02d" % (t // 60, t % 60)
            for a in LOGS[t]:
                ans.append(f"{k} {a}")
        return "\n".join(ans)

    def born(self, cmd: Commander):  # 出生

        cls = cmd.shape_clss[cmd.shape_idx % len(cmd.shape_clss)]
        if cmd.hp < cls.hp:
            return
        cmd.hp -= cls.hp
        cmd.shape_idx += 1
        s: Unit = cls(cmd)
        cmd.shape_map[cmd.color] = s
        s.action(Unit.BORN)

    def move(self, cmd: Commander):  # 移动
        if cmd.color == Commander.RED:
            start_idx, stop_idx, step = len(self.citys) - 2, -1, -1
        else:
            start_idx, stop_idx, step = 1, len(self.citys), 1
        while start_idx != stop_idx:
            cur_city = self.citys[start_idx]
            if cur_city.shape_map[cmd.color] is None:
                start_idx += step
                continue
            next_city = self.citys[start_idx - step]
            cur_city.shape_map[cmd.color].action(Unit.MARCHED, city=next_city)
            next_city.shape_map[cmd.color], cur_city.shape_map[cmd.color] = (
                cur_city.shape_map[cmd.color],
                None,
            )
            start_idx += step

    def do_when_0(self):
        for c in self.cmds:
            self.born(c)

    def do_when_10(self):
        for c in self.cmds:
            self.move(c)

    def do_when_20(self):
        for c in self.citys[1:-1]:
            c.hp += 10

    def do_when_30(self):

        for c in self.citys[1:-1]:
            s0, s1 = c.shape_map
            if s0 is None and s1:
                s1.action(Unit.earned)
            elif s1 is None and s0:
                s0.action(Unit.earned)

    def do_when_40(self):
        pass

    def do_when_50(self):
        for c in self.cmds:
            add_action(Action([f"{c.hp} elements in {c.color} headquarter"]))

    def main(self):
        cases, *args = self.ii()
        for i in range(cases):
            main_hp, city_num, t = self.ii()
            init_hps = self.ii()
            init_attack_power = self.ii()
            print(
                self.execute(main_hp, city_num, t, init_hps, init_attack_power, i + 1)
            )


if __name__ == "__main__":
    Solution().main()
