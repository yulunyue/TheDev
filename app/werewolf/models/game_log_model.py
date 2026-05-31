from common.tool.export import (
    SqliteDbStore,
    StrModel,
    NumberModel,
)
from common.util.export import time
from ..constant import C


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


GameLogModel.set_resource(C.WEREWOLF_DB)
