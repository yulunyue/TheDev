from common.tool.export import (
    SqliteDbStore,
    StrModel,
    NumberModel,
    SelectModel,
    DictModel,
)
from ..constant import Role, Phase, GameState, C
from .player_model import PlayerModel


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


RoomModel.set_resource(C.WEREWOLF_DB)
