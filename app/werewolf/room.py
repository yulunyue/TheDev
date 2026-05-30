from common.util.export import ApiBase, Node, IO_MANAGE, json, random, time, logger
from .model import RoomModel, PlayerModel, GameLogModel, AIMemoryModel
from .constant import Role, Phase, GameState, C
from .engine import GameEngine


class Room(ApiBase):
    ROUTE_PATH = "/werewolf/room"
    
    def start_game(self, room_id: str, **kw):
        room = RoomModel.get(room_id)
        if not room:
            return Node(ok=False, title="房间不存在")
        
        if room.host.get_value() != self.username:
            return Node(ok=False, title="只有房主可以开始游戏")
        
        players = PlayerModel.get_players_by_room(room_id)
        if len(players) < C.TOTAL_PLAYERS:
            return Node(ok=False, title=f"需要{C.TOTAL_PLAYERS}名玩家才能开始")
        
        not_ready = [p.username.get_value() for p in players if not p.is_ai.get_value() and not p.is_ready.get_value()]
        if not_ready:
            return Node(ok=False, title=f"以下玩家未准备: {', '.join(not_ready)}")
        
        engine = GameEngine(room_id)
        engine.start_game()
        
        return Node(ok=True, title="游戏已开始")
    
    def speech(self, room_id: str, content: str, **kw):
        room = RoomModel.get(room_id)
        if not room:
            return Node(ok=False, title="房间不存在")
        
        if room.phase.get_value() != Phase.DAY.value:
            return Node(ok=False, title="当前不是发言阶段")
        
        player = PlayerModel.get_player_by_room_username(room_id, self.username)
        if not player:
            return Node(ok=False, title="您不在该房间")
        
        if not player.is_alive.get_value():
            return Node(ok=False, title="您已死亡，无法发言")
        
        if player.seat.get_value() != room.current_speaker.get_value():
            return Node(ok=False, title="不是您的发言回合")
        
        GameLogModel.log_event(
            room_id=room_id,
            round_num=room.round_num.get_value(),
            phase=Phase.DAY.value,
            event_type=C.MSG_SPEECH,
            actor=self.username,
            content=content,
        )
        
        self._broadcast_room(room_id, C.MSG_SPEECH, {
            "seat": player.seat.get_value(),
            "username": self.username,
            "content": content,
        })
        
        engine = GameEngine(room_id)
        engine.next_speaker()
        
        return Node(ok=True)
    
    def vote(self, room_id: str, target_seat: int, **kw):
        room = RoomModel.get(room_id)
        if not room:
            return Node(ok=False, title="房间不存在")
        
        if room.phase.get_value() != Phase.VOTE.value:
            return Node(ok=False, title="当前不是投票阶段")
        
        player = PlayerModel.get_player_by_room_username(room_id, self.username)
        if not player:
            return Node(ok=False, title="您不在该房间")
        
        if not player.is_alive.get_value():
            return Node(ok=False, title="您已死亡，无法投票")
        
        if target_seat < 1 or target_seat > C.TOTAL_PLAYERS:
            return Node(ok=False, title="无效的座位号")
        
        target_player = PlayerModel.get_player_by_room_seat(room_id, target_seat)
        if not target_player or not target_player.is_alive.get_value():
            return Node(ok=False, title="目标玩家不存在或已死亡")
        
        GameLogModel.log_event(
            room_id=room_id,
            round_num=room.round_num.get_value(),
            phase=Phase.VOTE.value,
            event_type=C.MSG_VOTE,
            actor=self.username,
            target=str(target_seat),
            content=f"投票给{target_seat}号玩家",
        )
        
        self._broadcast_room(room_id, C.MSG_VOTE, {
            "seat": player.seat.get_value(),
            "username": self.username,
            "target_seat": target_seat,
        })
        
        engine = GameEngine(room_id)
        engine.process_vote(player.seat.get_value(), target_seat)
        
        return Node(ok=True)
    
    def night_action(self, room_id: str, action_type: str, target_seat: int = 0, **kw):
        room = RoomModel.get(room_id)
        if not room:
            return Node(ok=False, title="房间不存在")
        
        if room.phase.get_value() != Phase.NIGHT.value:
            return Node(ok=False, title="当前不是夜晚阶段")
        
        player = PlayerModel.get_player_by_room_username(room_id, self.username)
        if not player:
            return Node(ok=False, title="您不在该房间")
        
        if not player.is_alive.get_value():
            return Node(ok=False, title="您已死亡")
        
        role = player.role.get_value()
        
        engine = GameEngine(room_id)
        result = engine.night_action(player.seat.get_value(), role, action_type, target_seat)
        
        return Node(ok=result.get("ok", True), title=result.get("title", ""))
    
    def hunter_shot(self, room_id: str, target_seat: int, **kw):
        room = RoomModel.get(room_id)
        if not room:
            return Node(ok=False, title="房间不存在")
        
        player = PlayerModel.get_player_by_room_username(room_id, self.username)
        if not player:
            return Node(ok=False, title="您不在该房间")
        
        if player.role.get_value() != Role.HUNTER.value:
            return Node(ok=False, title="您不是猎人")
        
        if player.is_alive.get_value():
            return Node(ok=False, title="您还活着")
        
        target_player = PlayerModel.get_player_by_room_seat(room_id, target_seat)
        if not target_player or not target_player.is_alive.get_value():
            return Node(ok=False, title="目标玩家不存在或已死亡")
        
        engine = GameEngine(room_id)
        engine.hunter_shot(player.seat.get_value(), target_seat)
        
        return Node(ok=True, title="猎人开枪成功")
    
    def get_game_state(self, room_id: str, **kw):
        room = RoomModel.get(room_id)
        if not room:
            return Node(ok=False, title="房间不存在")
        
        player = PlayerModel.get_player_by_room_username(room_id, self.username)
        
        players = PlayerModel.get_players_by_room(room_id)
        logs = GameLogModel.get_logs_by_room(room_id, room.round_num.get_value())
        
        return Node(ok=True, data={
            "room": room.to_public_dict(),
            "players": [p.to_public_dict() for p in players],
            "my_info": player.to_private_dict() if player else None,
            "logs": [{"type": l.event_type.get_value(), "actor": l.actor.get_value(), 
                      "target": l.target.get_value(), "content": l.content.get_value()} for l in logs],
        })
    
    def finish_night_action(self, room_id: str, **kw):
        room = RoomModel.get(room_id)
        if not room:
            return Node(ok=False, title="房间不存在")
        
        if room.phase.get_value() != Phase.NIGHT.value:
            return Node(ok=False, title="当前不是夜晚阶段")
        
        player = PlayerModel.get_player_by_room_username(room_id, self.username)
        if not player:
            return Node(ok=False, title="您不在该房间")
        
        if not player.is_alive.get_value():
            return Node(ok=False, title="您已死亡")
        
        if player.is_ai.get_value():
            return Node(ok=False, title="AI玩家无需手动完成")
        
        engine = GameEngine(room_id)
        engine.finish_night_action(self.username)
        
        return Node(ok=True, title="夜晚行动已完成")
    
    def _broadcast_room(self, room_id: str, msg_type: str, data: dict):
        topic = f"{C.TOPIC_WEREWOLF_ROOM}_{room_id}"
        IO_MANAGE.send(topic, {"type": msg_type, **data})