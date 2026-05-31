from common.util.export import ApiBase, Node, IO_MANAGE, json, random, time, logger
from common.util.api.apicall import ApiCall
from .models import RoomModel, PlayerModel
from .constant import Role, Phase, GameState, C
from .engine import GameEngine


class Lobby(ApiBase):
    ROUTE_PATH = "/werewolf/lobby"
    
    def room_list(self, **kw):
        rooms = []
        for room in RoomModel.all():
            if room.state.get_value() != GameState.ENDED.value:
                rooms.append(room.to_public_dict())
        return Node(ok=True, data={"rooms": rooms})
    
    def create_room(self, name: str, **kw):
        existing = [r for r in RoomModel.all() if r.host.get_value() == self.username]
        for r in existing:
            if r.state.get_value() != GameState.ENDED.value:
                return Node(ok=False, title="您已有未结束的房间")
        
        room_id = f"room_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
        room = RoomModel.create_room(room_id, name, self.username)
        
        player_id = f"{room_id}_{self.username}"
        PlayerModel.create_player(player_id, room_id, self.username, seat=1, is_ai=False)
        
        self._subscribe_room(room_id)
        self._broadcast_lobby()
        
        return Node(ok=True, data={"room_id": room_id, "room": room.to_public_dict()})
    
    def join_room(self, room_id: str, seat: int = 0, **kw):
        if not RoomModel.exist(room_id):
            return Node(ok=False, title="房间不存在")
        
        room = RoomModel.get(room_id)
        
        if room.state.get_value() != GameState.WAITING.value:
            return Node(ok=False, title="游戏已开始，无法加入")
        
        existing = PlayerModel.get_player_by_room_username(room_id, self.username)
        players = PlayerModel.get_players_by_room(room_id)
        
        if seat > 0:
            if seat < 1 or seat > C.TOTAL_PLAYERS:
                return Node(ok=False, title=f"座位号必须在 1-{C.TOTAL_PLAYERS} 之间")
            
            if existing and existing.seat.get_value() == seat:
                self._subscribe_room(room_id)
                return Node(ok=True, data={"room_id": room_id, "room": room.to_public_dict()})
            
            others = [p for p in players if p.username.get_value() != self.username]
            for p in sorted(others, key=lambda p: p.seat.get_value(), reverse=True):
                s = p.seat.get_value()
                if s >= seat:
                    new_seat = s + 1
                    if new_seat > C.TOTAL_PLAYERS:
                        p.delete()
                    else:
                        p.seat.set_value(new_seat)
            PlayerModel.save_to_local()
        else:
            if len(players) >= C.TOTAL_PLAYERS:
                return Node(ok=False, title="房间已满")
            seat = max([p.seat.get_value() for p in players], default=0) + 1
        
        if existing:
            existing.seat.set_value(seat)
            existing.is_ready.set_value(False)
            PlayerModel.save_to_local()
        else:
            player_id = f"{room_id}_{self.username}"
            PlayerModel.create_player(player_id, room_id, self.username, seat=seat, is_ai=False)
        
        self._subscribe_room(room_id)
        self._broadcast_room(room_id, C.MSG_PLAYER_JOIN, {"username": self.username, "seat": seat})
        self._broadcast_lobby()
        
        return Node(ok=True, data={"room_id": room_id, "room": room.to_public_dict()})
    
    def leave_room(self, room_id: str, **kw):
        if not RoomModel.exist(room_id):
            return Node(ok=False, title="房间不存在")
        
        room = RoomModel.get(room_id)
        
        player = PlayerModel.get_player_by_room_username(room_id, self.username)
        if not player:
            return Node(ok=False, title="您不在该房间")
        
        if room.state.get_value() == GameState.GAMING.value and player.is_alive.get_value():
            return Node(ok=False, title="游戏进行中，无法离开")
        
        player.delete()
        PlayerModel.save_to_local()
        
        players = PlayerModel.get_players_by_room(room_id)
        if not players:
            room.delete()
            RoomModel.save_to_local()
        elif room.host.get_value() == self.username:
            new_host = players[0].username.get_value()
            room.host.set_value(new_host)
            RoomModel.save_to_local()
        
        self._broadcast_room(room_id, C.MSG_PLAYER_LEAVE, {"username": self.username})
        self._broadcast_lobby()
        
        return Node(ok=True)
    
    def get_room_info(self, room_id: str, **kw):
        if not RoomModel.exist(room_id):
            return Node(ok=False, title="房间不存在")
        
        room = RoomModel.get(room_id)
        
        players = PlayerModel.get_players_by_room(room_id)
        player = PlayerModel.get_player_by_room_username(room_id, self.username)
        
        confirmed_roles = {}
        if room.state.get_value() in (GameState.GAMING.value, GameState.ENDED.value) and player:
            confirmed_roles = GameEngine.get_confirmed_roles(room_id, room, player, players)
        
        return Node(ok=True, data={
            "room": room.to_public_dict(),
            "players": [p.to_public_dict() for p in players],
            "my_seat": player.seat.get_value() if player else 0,
            "is_in_room": player is not None,
            "my_info": player.to_public_dict() if player else None,
            "confirmed_roles": confirmed_roles,
        })
    
    def set_ready(self, room_id: str, ready: bool, **kw):
        player = PlayerModel.get_player_by_room_username(room_id, self.username)
        if not player:
            return Node(ok=False, title="您不在该房间")
        
        player.is_ready.set_value(ready)
        PlayerModel.save_to_local()
        
        self._broadcast_room(room_id, C.MSG_ROOM_UPDATE, {})
        
        return Node(ok=True)
    
    def add_ai_player(self, room_id: str, ai_persona: str = "", seat: int = 0, **kw):
        if not RoomModel.exist(room_id):
            return Node(ok=False, title="房间不存在")
        
        room = RoomModel.get(room_id)
        
        if room.host.get_value() != self.username:
            return Node(ok=False, title="只有房主可以添加AI")
        
        if room.state.get_value() != GameState.WAITING.value:
            return Node(ok=False, title="游戏已开始")
        
        players = PlayerModel.get_players_by_room(room_id)
        
        if seat > 0:
            if seat < 1 or seat > C.TOTAL_PLAYERS:
                return Node(ok=False, title=f"座位号必须在 1-{C.TOTAL_PLAYERS} 之间")
            others = [p for p in players if p.username.get_value() != self.username]
            for p in sorted(others, key=lambda p: p.seat.get_value(), reverse=True):
                s = p.seat.get_value()
                if s >= seat:
                    new_seat = s + 1
                    if new_seat > C.TOTAL_PLAYERS:
                        p.delete()
                    else:
                        p.seat.set_value(new_seat)
            PlayerModel.save_to_local()
        else:
            taken = {int(p.seat.get_value()) for p in players}
            for s in range(1, C.TOTAL_PLAYERS + 1):
                if s not in taken:
                    seat = s
                    break
            if not seat:
                return Node(ok=False, title="房间已满")
        ai_id = f"AI_{seat}"
        ai_username = f"{C.AI_NAME_PREFIX}{int(time.time() * 1000)}_{seat}"
        player_id = f"{room_id}_{ai_username}"
        
        personas = ["激进型", "保守型", "分析型", "煽动型", "沉默型", "活泼型"]
        if not ai_persona:
            ai_persona = random.choice(personas)
        
        PlayerModel.create_player(player_id, room_id, ai_username, seat=seat, is_ai=True, ai_persona=ai_persona)
        
        self._broadcast_room(room_id, C.MSG_PLAYER_JOIN, {"username": ai_username, "seat": seat, "is_ai": True, "ai_persona": ai_persona})
        self._broadcast_lobby()
        
        return Node(ok=True, data={"ai_username": ai_username, "seat": seat})
    
    def remove_ai_player(self, room_id: str, ai_username: str, **kw):
        if not RoomModel.exist(room_id):
            return Node(ok=False, title="房间不存在")
        
        room = RoomModel.get(room_id)
        
        if room.host.get_value() != self.username:
            return Node(ok=False, title="只有房主可以移除AI")
        
        player = PlayerModel.get_player_by_room_username(room_id, ai_username)
        if not player or not player.is_ai.get_value():
            return Node(ok=False, title="AI玩家不存在")
        
        player.delete()
        PlayerModel.save_to_local()
        
        self._broadcast_room(room_id, C.MSG_PLAYER_LEAVE, {"username": ai_username})
        self._broadcast_lobby()
        
        return Node(ok=True)
    
    def _subscribe_room(self, room_id: str):
        topic = f"{C.TOPIC_WEREWOLF_ROOM}_{room_id}"
        IO_MANAGE.sub(topic, self.username)
    
    def _broadcast_room(self, room_id: str, msg_type: str, data: dict):
        topic = f"{C.TOPIC_WEREWOLF_ROOM}_{room_id}"
        IO_MANAGE.send(topic, {"type": msg_type, **data})
    
    def _broadcast_lobby(self):
        rooms = [r.to_public_dict() for r in RoomModel.all() if r.state.get_value() != GameState.ENDED.value]
        IO_MANAGE.send(C.TOPIC_WEREWOLF_LOBBY, {"type": C.MSG_ROOM_UPDATE, "rooms": rooms})