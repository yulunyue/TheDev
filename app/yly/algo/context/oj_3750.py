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
        self.score = [0, 0]

    def __str__(self):
        return " ".join(self.msgs)

    def set_score(self, v):
        self.score[0] = v
        return self


LOGS: Dict[int, List[Action]] = dict()


def add_action(a: Action):
    if Solution.now_t not in LOGS:
        LOGS[Solution.now_t] = []
    a.score[1] = len(LOGS[Solution.now_t])
    LOGS[Solution.now_t].append(a)


class City:
    hp = 0

    def __init__(self, city_idx):
        self.city_idx = city_idx
        self.shape_map: List[Unit] = [None, None]
        self.flag = None

    def __str__(self):
        return f"city {self.city_idx}"

    def get_fight_id(self):
        if self.flag == Commander.RED:
            return self.shape_map
        if self.flag == Commander.BLUE:
            return self.shape_map[::-1]
        if self.city_idx % 2:
            return self.shape_map
        return self.shape_map[::-1]

    def fight(self):
        if not self.shape_map[0] or not self.shape_map[1]:
            return
        self_unit, op_unit = self.get_fight_id()
        self_unit.action(Unit.attacked, op_unit=op_unit)
        if self.kill(self_unit, op_unit, self_unit.attack_power, True):
            return
        if isinstance(op_unit, Ninja):
            return
        op_unit.action(Unit.fight_back, op_unit=self_unit)
        if not self.kill(op_unit, self_unit, op_unit.attack_power // 2, False):
            if isinstance(self_unit, Dragon):
                self_unit.action(Unit.yelled)

    last_win = None

    def kill(self, self_unit: "Unit", op_unit: "Unit", power, is_attack):
        op_unit_hp = op_unit.hp - power
        if op_unit_hp > 0:
            op_unit.hp = op_unit_hp
            return False
        if is_attack and isinstance(self_unit, Wolf):
            self_unit.attack_power *= 2
            self_unit.hp *= 2
        op_unit.action(Unit.killed, op_unit=self_unit)
        self_unit.capture_hp(False)
        if self.last_win is not None and self.last_win == self_unit.cmd.color:
            if self.flag != self_unit.cmd.color:
                self.flag = self_unit.cmd.color
                a = Action(
                    [self_unit.cmd.color_str, "flag raised in city", str(self.city_idx)]
                )
                add_action(a)
        self.last_win = self_unit.cmd.color
        op_unit.hp = 0
        return True


class Unit:
    attack_power: int = None
    hp: int = None
    type_name = ""
    BORN = "born"
    yelled = "yelled"
    MARCHED = "marched to"
    earned = "earned"
    attacked = "attacked"
    killed = "was killed"
    fight_back = "fought back against"
    reached = "reached"

    def __init__(self, city: "City"):
        self.cmd: Commander = city
        self.city: City = city
        self.key = self.cmd.shape_idx

    def k(self):
        return [
            self.cmd.color_str,
            self.type_name,
            str(self.key),
        ]

    def action(self, s, city=None, op_unit: "Unit" = None):
        ret = self.k() + [s]
        if s == self.MARCHED or s == self.reached:
            ret.extend([str(city), self.info()])
            self.city = city
        elif s == self.earned:
            ret += [f"{self.city.hp} elements for his headquarter"]
        elif s == self.attacked or s == self.fight_back:
            ret += op_unit.k() + [f"in city {self.city.city_idx}"]
            if s == self.attacked:
                ret += [self.info()]
        elif s == self.killed:
            op_unit.cmd.kill_op_units.append(op_unit)
            self.city.shape_map[self.cmd.color] = None
            ret += [f"in city {self.city.city_idx}"]
        elif s == self.yelled:
            ret += [f"in city {self.city.city_idx}"]
        a = Action(ret)
        add_action(a)
        return a

    def capture_hp(self, cp_now=True):
        self.action(self.earned)
        if cp_now:
            self.cmd.hp += self.city.hp
        else:
            self.cmd.tmp_hp += self.city.hp
        self.city.hp = 0

    def info(self):
        return f"with {self.hp} elements and force {self.attack_power}"

    def move(self, next_city: "City"):
        self.city.shape_map[self.cmd.color] = None
        if isinstance(next_city, Commander):
            a = self.action(Unit.reached, city=next_city)
            next_city.op_count += 1
            if next_city.op_count >= 2:
                a = Action([f"{next_city.color_str} headquarter was taken"])
                add_action(a)

        else:
            a = self.action(Unit.MARCHED, city=next_city)
        a.set_score(next_city.city_idx)
        next_city.shape_map[self.cmd.color] = self


class Dragon(Unit):
    type_name = "dragon"


class Ninja(Unit):
    type_name = "ninja"


class IceMan(Unit):
    type_name = "iceman"

    def move(self, next_city):
        move_num = abs(next_city.city_idx - self.cmd.city_idx)
        if move_num % 2 == 0 and move_num:
            self.hp = max(self.hp - 9, 1)
            self.attack_power += 20
        return super().move(next_city)


class Lion(Unit):
    type_name = "lion"

    def action(self, s, city=None, op_unit=None):
        if s == self.killed:
            op_unit.hp += self.hp
        return super().action(s, city, op_unit)


class Wolf(Unit):
    type_name = "wolf"


SHAPES: List[Unit] = [Dragon, Ninja, IceMan, Lion, Wolf]


class Commander(City):
    RED = 0
    BLUE = 1

    def __init__(self, color, hp, city_idx):
        self.hp = hp
        self.color = color
        self.tmp_hp: int = 0
        self.kill_op_units: List[Unit] = []
        if self.color == Commander.RED:
            self.shape_clss: List[Unit] = [IceMan, Lion, Wolf, Ninja, Dragon]
        else:
            self.shape_clss: List[Unit] = [Lion, Dragon, Ninja, IceMan, Wolf]
        self.shape_idx = 0
        self.op_count = 0
        # self.shapes_all: Dict[int, Unit] = {}
        super().__init__(city_idx)

    @property
    def color_str(self):
        return "red" if self.color == Commander.RED else "blue"

    def __str__(self):
        return f"{self.color_str} headquarter"


class Solution(MockCf):
    now_t = 0
    uri = "http://bailian.openjudge.cn/practice/3750/|https://www.luogu.com.cn/problem/U275831"

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
            dict(
                main_hp=40,
                city_num=1,
                t=1000,
                init_hps=[20, 20, 20, 20, 20],
                init_attack_power=[20, 20, 20, 20, 20],
                result=O2,
                case_id=2,
            ),
        ]

    def execute(self, main_hp, city_num, t, init_hps, init_attack_power, case_id):
        self.city_num = city_num
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
            for a in sorted(LOGS[t], key=lambda a: a.score):
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
            cur_city.shape_map[cmd.color].move(self.citys[start_idx - step])
            start_idx += step

    def do_when_0(self):
        for c in self.cmds:
            self.born(c)

    def do_when_10(self):
        for c in self.cmds:
            self.move(c)
        if self.cmds[0].op_count >= 2 or self.cmds[1].op_count >= 2:
            return True

    def do_when_20(self):
        for c in self.citys[1:-1]:
            c.hp += 10

    def do_when_30(self):

        for c in self.citys[1:-1]:
            s0, s1 = c.shape_map
            if s0 is None and s1:
                s1.capture_hp()
            elif s1 is None and s0:
                s0.capture_hp()

    def do_when_40(self):
        for c in self.citys[1:-1]:
            c.fight()

    def do_when_50(self):
        for c in self.cmds:
            c.kill_op_units.sort(
                key=lambda v: abs(
                    v.city.city_idx - (self.city_num + 1 - v.cmd.city_idx)
                )
            )
            for u in c.kill_op_units:
                if c.hp < 8:
                    break
                c.hp -= 8
                u.hp += 8
            c.hp += c.tmp_hp
            add_action(Action([f"{c.hp} elements in {c}"]))
            c.kill_op_units = []
            c.tmp_hp = 0

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
