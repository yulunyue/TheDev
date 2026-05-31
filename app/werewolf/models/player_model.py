from common.tool.export import (
    SqliteDbStore,
    StrModel,
    NumberModel,
    BoolModel,
    SelectModel,
)
from ..constant import Role, C


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


PlayerModel.set_resource(C.WEREWOLF_DB)
