from common.tool.export import (
    SqliteDbStore,
    StrModel,
    NumberModel,
)
from common.util.export import time
from ..constant import C


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


AIMemoryModel.set_resource(C.WEREWOLF_DB)
