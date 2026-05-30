from common.tool.export import (
    SqliteDbStore,
    StrModel,
    NumberModel,
    BoolModel,
    ListModel,
    DictModel,
    SelectModel,
)
from common.util.export import json, time
from .constant import Role, Phase, GameState, C


class RoomModel(SqliteDbStore):
    name = StrModel().set_title("房间名称")
    host = StrModel().set_title("房主")
    state = SelectModel().set_options(
        GameState.WAITING.value, GameState.GAMING.value, GameState.ENDED.value
    ).set_title("房间状态")
    phase = SelectModel().set_options(
        Phase.WAITING.value,
        Phase.PREPARING.value,
        Phase.NIGHT.value,
        Phase.DAY.value,
        Phase.VOTE.value,
        Phase.RESULT.value,
    ).set_title("游戏阶段")
    round_num = NumberModel(default_value=0).set_title("当前回合")
    config = DictModel().set_title("游戏配置")
    current_speaker = NumberModel(default_value=0).set_title("当前发言者座位")
    vote_target = StrModel().set_title("当前投票目标")
    night_actions = DictModel().set_title("夜晚行动记录")
    day_time = NumberModel(default_value=0).set_title("白天开始时间")
    
    @classmethod
    def create_room(cls, room_id: str, name: str, host: str, config: dict = None):
        if config is None:
            config = C.ROLE_CONFIG_9
        room = cls.get(room_id)
        room.name.set_value(name)
        room.host.set_value(host)
        room.state.set_value(GameState.WAITING.value)
        room.phase.set_value(Phase.WAITING.value)
        room.round_num.set_value(0)
        room.config.set_value({k.value if isinstance(k, Role) else k: v for k, v in config.items()})
        room.current_speaker.set_value(0)
        room.vote_target.set_value("")
        room.night_actions.set_value({})
        room.day_time.set_value(0)
        cls.save_to_local()
        return room
    
    def to_public_dict(self):
        return {
            "id": self._id,
            "name": self.name.get_value(),
            "host": self.host.get_value(),
            "state": self.state.get_value(),
            "phase": self.phase.get_value(),
            "round_num": self.round_num.get_value(),
            "player_count": len(PlayerModel.get_players_by_room(self._id)),
        }


class PlayerModel(SqliteDbStore):
    room_id = StrModel().set_title("所属房间")
    username = StrModel().set_title("用户名")
    seat = NumberModel(default_value=0).set_title("座位号")
    role = SelectModel().set_options(
        Role.UNSET.value,
        Role.WOLF.value,
        Role.SEER.value,
        Role.WITCH.value,
        Role.GUARD.value,
        Role.HUNTER.value,
        Role.VILLAGER.value,
    ).set_title("角色")
    is_alive = BoolModel(default_value=True).set_title("是否存活")
    is_ai = BoolModel(default_value=False).set_title("是否AI")
    ai_persona = StrModel().set_title("AI性格")
    is_ready = BoolModel(default_value=False).set_title("是否准备")
    
    @classmethod
    def create_player(cls, player_id: str, room_id: str, username: str, seat: int, is_ai: bool = False, ai_persona: str = ""):
        player = cls.get(player_id)
        player.room_id.set_value(room_id)
        player.username.set_value(username)
        player.seat.set_value(seat)
        player.is_alive.set_value(True)
        player.is_ai.set_value(is_ai)
        player.ai_persona.set_value(ai_persona)
        player.is_ready.set_value(is_ai)
        player.role.set_value(Role.UNSET.value)
        cls.save_to_local()
        return player
    
    @classmethod
    def get_players_by_room(cls, room_id: str):
        return [p for p in cls.all() if p.room_id.get_value() == room_id]
    
    @classmethod
    def get_player_by_room_seat(cls, room_id: str, seat: int):
        for p in cls.all():
            if p.room_id.get_value() == room_id and p.seat.get_value() == seat:
                return p
        return None
    
    @classmethod
    def get_player_by_room_username(cls, room_id: str, username: str):
        for p in cls.all():
            if p.room_id.get_value() == room_id and p.username.get_value() == username:
                return p
        return None
    
    def to_public_dict(self):
        return {
            "id": self._id,
            "username": self.username.get_value(),
            "seat": self.seat.get_value(),
            "is_alive": self.is_alive.get_value(),
            "is_ai": self.is_ai.get_value(),
            "is_ready": self.is_ready.get_value(),
        }
    
    def to_private_dict(self):
        return {
            "id": self._id,
            "username": self.username.get_value(),
            "seat": self.seat.get_value(),
            "role": self.role.get_value(),
            "is_alive": self.is_alive.get_value(),
            "is_ai": self.is_ai.get_value(),
        }


class GameLogModel(SqliteDbStore):
    room_id = StrModel().set_title("所属房间")
    round_num = NumberModel(default_value=0).set_title("回合")
    phase = StrModel().set_title("阶段")
    event_type = StrModel().set_title("事件类型")
    actor = StrModel().set_title("执行者")
    target = StrModel().set_title("目标")
    content = StrModel().set_title("内容")
    timestamp = NumberModel(default_value=0).set_title("时间戳")
    
    @classmethod
    def log_event(cls, room_id: str, round_num: int, phase: str, event_type: str, 
                  actor: str = "", target: str = "", content: str = ""):
        log_id = f"{room_id}_{round_num}_{phase}_{event_type}_{int(time.time()*1000)}"
        log = cls.get(log_id)
        log.room_id.set_value(room_id)
        log.round_num.set_value(round_num)
        log.phase.set_value(phase)
        log.event_type.set_value(event_type)
        log.actor.set_value(actor)
        log.target.set_value(target)
        log.content.set_value(content)
        log.timestamp.set_value(int(time.time() * 1000))
        cls.save_to_local()
        return log
    
    @classmethod
    def get_logs_by_room(cls, room_id: str, round_num: int = None):
        logs = []
        for log in cls.all():
            if log.room_id.get_value() == room_id:
                if round_num is None or log.round_num.get_value() == round_num:
                    logs.append(log)
        return sorted(logs, key=lambda x: x.timestamp.get_value())


class AIMemoryModel(SqliteDbStore):
    room_id = StrModel().set_title("所属房间")
    player_id = StrModel().set_title("AI玩家ID")
    round_num = NumberModel(default_value=0).set_title("回合")
    memory_type = StrModel().set_title("记忆类型")
    content = StrModel().set_title("记忆内容")
    timestamp = NumberModel(default_value=0).set_title("时间戳")
    
    @classmethod
    def add_memory(cls, room_id: str, player_id: str, round_num: int, 
                   memory_type: str, content: str):
        mem_id = f"{room_id}_{player_id}_{round_num}_{memory_type}_{int(time.time()*1000)}"
        mem = cls.get(mem_id)
        mem.room_id.set_value(room_id)
        mem.player_id.set_value(player_id)
        mem.round_num.set_value(round_num)
        mem.memory_type.set_value(memory_type)
        mem.content.set_value(content)
        mem.timestamp.set_value(int(time.time() * 1000))
        cls.save_to_local()
        return mem
    
    @classmethod
    def get_memories(cls, room_id: str, player_id: str, round_num: int = None):
        memories = []
        for mem in cls.all():
            if mem.room_id.get_value() == room_id and mem.player_id.get_value() == player_id:
                if round_num is None or mem.round_num.get_value() <= round_num:
                    memories.append(mem)
        return sorted(memories, key=lambda x: x.timestamp.get_value())


AI_MEMORY = {}


RoomModel.set_resource("data/werewolf/room.db")
PlayerModel.set_resource("data/werewolf/player.db")
GameLogModel.set_resource("data/werewolf/game_log.db")
AIMemoryModel.set_resource("data/werewolf/ai_memory.db")