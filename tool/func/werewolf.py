import json
import os

from common.tool.export import ToolBase
from common.util.export import logger


class WerewolfTool(ToolBase):
    name = "werewolf"
    TOTAL = 9

    def _lobby(self, username):
        from app.werewolf.lobby import Lobby
        return Lobby()._set_env(username)

    def _room(self, username):
        from app.werewolf.room import Room
        return Room()._set_env(username)

    def _cfg_path(self):
        d = f"data/tool/{self.__class__.__name__}"
        os.makedirs(d, exist_ok=True)
        return f"{d}/config.json"

    def _load_cfg(self):
        p = self._cfg_path()
        if os.path.exists(p):
            with open(p) as f:
                return json.load(f)
        return {}

    def _save_cfg(self, **kw):
        cfg = self._load_cfg()
        cfg.update(kw)
        with open(self._cfg_path(), "w") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)

    def _get(self, key, kw, default=""):
        val = kw.get(key)
        if val is not None:
            self._save_cfg(**{key: val})
            return val
        cfg = self._load_cfg()
        return cfg.get(key, default)

    def _id(self, kw):
        return self._get("room_id", kw)

    def _user(self, kw):
        return self._get("username", kw)

    def _echo(self, node, show_data=True):
        if node.ok is False:
            print(f"失败: {node.title}")
        elif node.ok is True:
            if node.title:
                print(f"成功: {node.title}")
            if show_data:
                data = node.get_data()
                if data:
                    print(data)
        else:
            data = node.get_data()
            if data:
                print(data)

    def _p(self, *args, **kw):
        print(*args, **kw)

    def _int(self, v):
        if isinstance(v, float):
            return int(v)
        return v

    def _save_room_id(self, data):
        rid = None
        if isinstance(data, dict):
            rid = data.get("room_id")
        elif isinstance(data, str):
            rid = data
        if rid:
            self._save_cfg(room_id=rid)

    def defaults(self, **kw):
        cfg = self._load_cfg()
        self._p(f"当前默认配置:")
        self._p(f"  room_id: {cfg.get('room_id', '(未设置)')}")
        self._p(f"  username: {cfg.get('username', '(未设置)')}")

    def set_default(self, **kw):
        before = self._load_cfg()
        after = {**before, **{k: v for k, v in kw.items() if v}}
        self._save_cfg(**after)
        self._p("已更新默认配置:")
        for k, v in after.items():
            self._p(f"  {k}: {v}")

    def room_list(self, **kw):
        username = self._user(kw)
        result = self._lobby(username).room_list()
        if not result.ok:
            self._p(f"失败: {result.title}")
            return
        data = result.get_data()
        rooms = data.get("rooms", [])
        if not rooms:
            self._p("暂无房间")
            return
        self._p(f"共 {len(rooms)} 个房间:")
        for r in rooms:
            self._p(f"  [{r['id']}] {r['name']} - 房主:{r['host']} 人数:{self._int(r['player_count'])} 状态:{r['state']}")

    def create_room(self, name, **kw):
        username = self._user(kw)
        result = self._lobby(username).create_room(name)
        if not result.ok:
            self._p(f"失败: {result.title}")
            return
        data = result.get_data()
        room_id = data.get("room_id", "")
        self._save_cfg(room_id=room_id, username=username)
        self._p(f"房间已创建: {room_id}")
        self._p(f"名称: {name}  房主: {username}")

        for seat in range(2, self.TOTAL + 1):
            self._lobby(username).add_ai_player(room_id)
        self._p("已自动填充 AI 玩家到满员")

        self._show_room_seats(room_id)

    def seats(self, **kw):
        room_id = self._id(kw)
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        self._show_room_seats(room_id)

    def _show_room_seats(self, room_id):
        from app.werewolf.models import RoomModel, PlayerModel
        if not RoomModel.exist(room_id):
            self._p("房间不存在")
            return
        players = PlayerModel.get_players_by_room(room_id)
        seat_map = {}
        for p in players:
            seat_map[self._int(p.seat.get_value())] = p
        self._p(f"\n房间席位 (共 {self.TOTAL} 座):")
        for s in range(1, self.TOTAL + 1):
            if s in seat_map:
                p = seat_map[s]
                tag = "AI" if p.is_ai.get_value() else "人"
                self._p(f"  {s}号: [{tag}] {p.username.get_value()}")
            else:
                self._p(f"  {s}号: [空]")

    def join_room(self, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        seat = int(kw.get("seat", 0))
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        result = self._lobby(username).join_room(room_id, seat)
        self._echo(result)
        if result.ok:
            self._show_room_seats(room_id)

    def leave_room(self, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        result = self._lobby(username).leave_room(room_id)
        self._echo(result)

    def room_info(self, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        result = self._lobby(username).get_room_info(room_id)
        if not result.ok:
            self._p(f"失败: {result.title}")
            return
        data = result.get_data()
        room = data.get("room", {})
        players = data.get("players", [])
        my_seat = data.get("my_seat", 0)
        confirmed_roles = data.get("confirmed_roles", {})
        self._p(f"房间: {room.get('name', '')} ({room_id})")
        self._p(f"状态: {room.get('state', '')} / {room.get('phase', '')}")
        self._p(f"房主: {room.get('host', '')}  回合: {self._int(room.get('round_num', 0))}")
        self._p(f"玩家 ({len(players)}人):")
        for p in players:
            tag = ""
            if self._int(p["seat"]) == my_seat:
                tag = " ← 你"
            if confirmed_roles and str(p["seat"]) in confirmed_roles:
                tag += f" [{confirmed_roles[str(p['seat'])]}]"
            self._p(f"  {self._int(p['seat'])}号: {p['username']}{' (AI)' if p.get('is_ai') else ''}{' ✅' if p.get('is_ready') else ''}{' ❤️' if p.get('is_alive') else ' 💀'}{tag}")

    def set_ready(self, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        ready = kw.get("ready", "true")
        val = ready.lower() in ("true", "1", "yes")
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        result = self._lobby(username).set_ready(room_id, val)
        self._echo(result, show_data=False)

    def add_ai(self, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        result = self._lobby(username).add_ai_player(room_id, kw.get("ai_persona", ""))
        self._echo(result)

    def remove_ai(self, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        ai_username = kw.get("ai_username", "")
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        if not ai_username:
            self._p("请指定 ai_username")
            return
        result = self._lobby(username).remove_ai_player(room_id, ai_username)
        self._echo(result)

    def start_game(self, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        result = self._room(username).start_game(room_id)
        self._echo(result, show_data=False)
        if result.ok:
            self._show_room_seats(room_id)

    def game_state(self, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        result = self._room(username).get_game_state(room_id)
        if not result.ok:
            self._p(f"失败: {result.title}")
            return
        data = result.get_data()
        room = data.get("room", {})
        players = data.get("players", [])
        my_info = data.get("my_info", {})
        logs = data.get("logs", [])
        confirmed_roles = data.get("confirmed_roles", {})

        self._p(f"=== 房间 {room_id} ===")
        self._p(f"阶段: {room.get('phase', '')}  回合: {self._int(room.get('round_num', 0))}")
        self._p(f"当前发言: {self._int(room.get('current_speaker', 0))}号")

        if my_info:
            role = my_info.get("role", "unknown")
            seat = self._int(my_info.get("seat", 0))
            alive = "存活" if my_info.get("is_alive") else "死亡"
            self._p(f"你: {seat}号 {role} ({alive})")

        self._p(f"\n玩家列表:")
        for p in players:
            tag = ""
            if self._int(p["seat"]) == self._int(my_info.get("seat", 0)):
                tag = " ← 你"
            if confirmed_roles and str(p["seat"]) in confirmed_roles:
                tag += f" [{confirmed_roles[str(p['seat'])]}]"
            self._p(f"  {self._int(p['seat'])}号: {p['username']}{' (AI)' if p.get('is_ai') else ''}{' ❤️' if p.get('is_alive') else ' 💀'}{tag}")

        if logs:
            self._p(f"\n日志:")
            for log in logs[-5:]:
                self._p(f"  {log.get('actor', '')}: {log.get('content', log.get('type', ''))}")

    def speech(self, content, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        result = self._room(username).speech(room_id, content)
        self._echo(result, show_data=False)

    def vote(self, target_seat, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        result = self._room(username).vote(room_id, int(target_seat))
        self._echo(result, show_data=False)

    def night_action(self, action_type, target_seat, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        result = self._room(username).night_action(room_id, action_type, int(target_seat))
        self._echo(result, show_data=False)

    def hunter_shot(self, target_seat, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        result = self._room(username).hunter_shot(room_id, int(target_seat))
        self._echo(result, show_data=False)

    def finish_night(self, **kw):
        room_id = self._id(kw)
        username = self._user(kw)
        if not room_id:
            self._p("请指定 room_id 或先设默认值")
            return
        result = self._room(username).finish_night_action(room_id)
        self._echo(result, show_data=False)

    def play(self, **kw):
        import time

        room_id = self._id(kw)
        username = self._user(kw)

        lobby = self._lobby(username)
        room_api = self._room(username)

        if not room_id:
            name = kw.get("name", f"{username}的狼人局")
            ret = lobby.create_room(name)
            if not ret.ok:
                self._p(f"创建房间失败: {ret.title}")
                return
            room_id = ret.get_data().get("room_id", "")
            self._save_cfg(room_id=room_id, username=username)
            self._p(f"创建房间: {name} ({room_id})")
            for _ in range(2, self.TOTAL + 1):
                lobby.add_ai_player(room_id)
            lobby.set_ready(room_id, True)
            ret = room_api.start_game(room_id)
            if not ret.ok:
                self._p(f"开局失败: {ret.title}")
                return
            self._show_room_seats(room_id)
            self._p("游戏已开始！")
        else:
            join_ret = lobby.join_room(room_id)
            if not join_ret.ok and "不在" not in (join_ret.title or ""):
                self._p(f"加入房间失败: {join_ret.title}")
                return
            self._p(f"进入房间 {room_id}，用户: {username}")

        last_phase = None

        while True:
            result = room_api.get_game_state(room_id)
            if not result.ok:
                self._p(f"获取状态失败: {result.title}")
                time.sleep(1)
                continue

            gs = result.get_data()
            rs = gs.get("room", {})
            phase = rs.get("phase", "")
            game_state = rs.get("state", "")
            current_speaker = rs.get("current_speaker", 0)
            round_num = rs.get("round_num", 0)
            players = gs.get("players", [])
            my_info = gs.get("my_info", {})
            logs = gs.get("logs", [])
            confirmed = gs.get("confirmed_roles", {})

            my_role = my_info.get("role", "") if my_info else ""
            my_seat = my_info.get("seat", 0) if my_info else 0
            is_alive = my_info.get("is_alive", True) if my_info else True
            is_ai = my_info.get("is_ai", False) if my_info else False

            if game_state == "ended":
                self._p("\n=== 游戏结束 ===")
                for p in players:
                    status = "存活" if p.get("is_alive") else "死亡"
                    self._p(f"  {self._int(p['seat'])}号 {p['username']} ({p.get('role', '?')}) {status}")
                break

            if is_ai:
                self._p("AI玩家，无需操作")
                break

            if phase != last_phase:
                self._p(f"\n--- 第{round_num}轮 阶段: {phase} ---")
                alive = [p for p in players if p.get("is_alive")]
                self._p("存活: " + ", ".join(f"{self._int(p['seat'])}号:{p['username']}" for p in alive))
                if my_role and my_role != "unset":
                    self._p(f"你的角色: {my_role} (座位{my_seat})")
                last_phase = phase

            if phase == "night":
                if not is_alive:
                    self._p("你已死亡，等待夜晚结束...")
                    time.sleep(2)
                    continue

                self._p("\n=== 夜晚行动 ===")
                actions_map = {
                    "wolf": [("kill", "击杀一个玩家")],
                    "seer": [("check", "查验一个玩家的身份")],
                    "witch": [("save", "救被杀的玩家"), ("poison", "毒杀一个玩家")],
                    "guard": [("protect", "守护一个玩家")],
                    "hunter": [],
                    "villager": [],
                }

                role_actions = actions_map.get(my_role, [])
                if not role_actions:
                    self._p(f"村民夜晚无行动，等待...")
                    room_api.finish_night_action(room_id)
                    time.sleep(2)
                    continue

                alive_others = [p for p in players if p.get("is_alive") and self._int(p["seat"]) != my_seat]
                for act, desc in role_actions:
                    self._p(f"\n[{act}] {desc}")
                    if my_role == "witch" and act == "save":
                        self._p("有人被杀了！是否使用解药？(y/n): ", end="")
                        choice = input().strip().lower()
                        if choice in ("y", "yes"):
                            from app.werewolf.models import RoomModel
                            rm = RoomModel.get(room_id)
                            na = rm.night_actions.get_value() or {}
                            wk = na.get("wolf_kill", [])
                            if wk:
                                target = wk[-1].get("target", 0)
                                self._p(f"救活 {self._int(target)} 号玩家")
                                room_api.night_action(room_id, "save", int(target))
                            else:
                                self._p("暂无人被杀")
                        continue

                    for p in alive_others:
                        tag = ""
                        if confirmed and str(p["seat"]) in confirmed:
                            tag = f" [{confirmed[str(p['seat'])]}]"
                        self._p(f"  {self._int(p['seat'])}号: {p['username']}{tag}")
                    self._p("输入目标座位号 (或直接回车跳过): ", end="")
                    inp = input().strip()
                    if inp:
                        room_api.night_action(room_id, act, int(inp))

                room_api.finish_night_action(room_id)
                self._p("夜晚行动完成，等待天亮...")

            elif phase == "day":
                if not is_alive:
                    self._p("你已死亡，等待白天结束...")
                    time.sleep(2)
                    continue

                if self._int(current_speaker) == my_seat:
                    self._p("\n=== 轮到你了！发言 ===")
                    content = input("发言内容: ").strip()
                    if content:
                        room_api.speech(room_id, content)
                        self._p("发言完成")
                else:
                    speaker = None
                    for p in players:
                        if self._int(p.get("seat")) == self._int(current_speaker):
                            speaker = p
                            break
                    if speaker:
                        name = speaker["username"]
                        tag = " (AI)" if speaker.get("is_ai") else ""
                        self._p(f"当前发言: {self._int(current_speaker)}号 {name}{tag}")
                    else:
                        self._p("等待发言...")
                    time.sleep(2)

            elif phase == "vote":
                if not is_alive:
                    self._p("你已死亡，跳过投票")
                    time.sleep(1)
                    continue

                self._p("\n=== 投票阶段 ===")
                alive_others = [p for p in players if p.get("is_alive") and self._int(p["seat"]) != my_seat]
                for p in alive_others:
                    tag = ""
                    if confirmed and str(p["seat"]) in confirmed:
                        tag = f" [{confirmed[str(p['seat'])]}]"
                    self._p(f"  {self._int(p['seat'])}号: {p['username']}{tag}")
                self._p("投票给几号? (输入0弃权): ", end="")
                inp = input().strip()
                if inp and int(inp) > 0:
                    room_api.vote(room_id, int(inp))
                    self._p("投票完成，等待结果...")
                time.sleep(1)

            elif phase == "result":
                self._p("结算中...")
                time.sleep(1)

            else:
                time.sleep(1)

            time.sleep(0.5)


if __name__ == "__main__":
    WerewolfTool().run()
