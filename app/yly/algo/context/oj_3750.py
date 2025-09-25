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
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


LOGS: Dict[int, List[Action]] = dict()


def add_action(a: Action):
    if Solution.now_t not in LOGS:
        LOGS[Solution.now_t] = []
    LOGS[Solution.now_t].append(a)


class Unit:
    attack_power: int = None
    init_hp: int = None
    type_name = ""


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


class Commander:
    RED = 1
    BLUE = 0

    def __init__(self, key, hp):
        self.hp = hp
        self.key = key
        if key == Commander.RED:
            self.shape_clss: List[Unit] = [IceMan, Lion, Wolf, Ninja, Dragon]
            self.color = "red"
        else:
            self.shape_clss: List[Unit] = [Lion, Ninja, Dragon, IceMan, Wolf]
            self.color = "blue"
        self.shapes = []
        self.born_idx = 0

    def born(self):
        s: Unit = self.shape_clss[self.born_idx]()
        self.shapes.append(s)
        add_action(Action(f"{self.color} {s.type_name} 1 born"))
        self.born_idx = (self.born_idx + 1) % len(self.shape_clss)


class Solution(MockCf):
    now_t = 0

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
            Commander(Commander.RED, main_hp),
            Commander(Commander.BLUE, main_hp),
        ]
        self.city_num, self.max_t = city_num, t
        for i, v in enumerate(SHAPES):
            v.attack_power, v.init_hp = init_attack_power[i], init_hps[i]
        LOGS.clear()
        Solution.now_t = 0
        while Solution.now_t < self.max_t:
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

    def do_when_0(self):
        self.cmds[0].born()
        self.cmds[1].born()

    def do_when_10(self):
        pass

    def do_when_20(self):
        pass

    def do_when_30(self):
        pass

    def do_when_40(self):
        pass

    def do_when_50(self):
        pass

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
