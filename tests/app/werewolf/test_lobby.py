import os
import sys
import tempfile
from common.util.export import TestBase, assert_dict, json
from app.werewolf.model import RoomModel, PlayerModel
from app.werewolf.constant import Role, Phase, GameState, C
from app.werewolf.lobby import Lobby


class TestLobby(TestBase):
    test_db_path = None
    
    @classmethod
    def setup_class(cls):
        cls.test_db_path = tempfile.mkdtemp(prefix="werewolf_lobby_test_")
        RoomModel.set_resource(os.path.join(cls.test_db_path, "room.db"))
        PlayerModel.set_resource(os.path.join(cls.test_db_path, "player.db"))
        RoomModel.init_resource()
        PlayerModel.init_resource()
    
    @classmethod
    def teardown_class(cls):
        if cls.test_db_path and os.path.exists(cls.test_db_path):
            import shutil
            shutil.rmtree(cls.test_db_path)
    
    def setup_method(self):
        RoomModel._config = {}
        RoomModel.instance_map = {}
        PlayerModel._config = {}
        PlayerModel.instance_map = {}
        for room in list(RoomModel.all()):
            room.delete()
        for player in list(PlayerModel.all()):
            player.delete()
        RoomModel.save_to_local()
        PlayerModel.save_to_local()
    
    def test_lobby_create_room_success(self):
        lobby = Lobby()
        lobby.username = "test_user_1"
        
        result = lobby.create_room(name="测试房间")
        
        self.expect(result.ok, True)
        self.expect("room_id" in result.data, True)
        self.expect("room" in result.data, True)
    
    def test_lobby_create_room_player_created(self):
        lobby = Lobby()
        lobby.username = "test_user_2"
        
        result = lobby.create_room(name="测试房间2")
        room_id = result.data["room_id"]
        
        player = PlayerModel.get_player_by_room_username(room_id, "test_user_2")
        self.expect(player is not None, True)
        self.expect(player.seat.get_value(), 1)
        self.expect(player.is_ai.get_value(), False)
        self.expect(player.role.get_value(), Role.UNSET.value)
    
    def test_lobby_create_room_state_waiting(self):
        lobby = Lobby()
        lobby.username = "test_user_3"
        
        result = lobby.create_room(name="测试房间3")
        room_id = result.data["room_id"]
        
        room = RoomModel.get(room_id)
        self.expect(room.state.get_value(), GameState.WAITING.value)
        self.expect(room.phase.get_value(), Phase.WAITING.value)
        self.expect(room.host.get_value(), "test_user_3")
    
    def test_lobby_create_room_duplicate_host(self):
        lobby = Lobby()
        lobby.username = "test_user_4"
        
        lobby.create_room(name="房间1")
        result2 = lobby.create_room(name="房间2")
        
        self.expect(result2.ok, False)
        self.expect("已有未结束的房间" in result2.title, True)
    
    def test_lobby_join_room_success(self):
        lobby1 = Lobby()
        lobby1.username = "host_user"
        result1 = lobby1.create_room(name="测试房间")
        room_id = result1.data["room_id"]
        
        lobby2 = Lobby()
        lobby2.username = "join_user"
        result2 = lobby2.join_room(room_id=room_id)
        
        self.expect(result2.ok, True)
        
        player = PlayerModel.get_player_by_room_username(room_id, "join_user")
        self.expect(player is not None, True)
        self.expect(player.seat.get_value(), 2)
        self.expect(player.role.get_value(), Role.UNSET.value)
    
    def test_lobby_join_room_not_exist(self):
        lobby = Lobby()
        lobby.username = "join_user_2"
        
        result = lobby.join_room(room_id="not_exist_room")
        
        self.expect(result.ok, False)
        self.expect("房间不存在" in result.title, True)
    
    def test_lobby_join_room_already_in_room(self):
        lobby = Lobby()
        lobby.username = "already_user"
        result1 = lobby.create_room(name="房间")
        room_id = result1.data["room_id"]
        
        result2 = lobby.join_room(room_id=room_id)
        
        self.expect(result2.ok, True)
        
        players = PlayerModel.get_players_by_room(room_id)
        self.expect(len(players), 1)
    
    def test_lobby_join_room_full(self):
        lobby = Lobby()
        lobby.username = "host_full"
        result = lobby.create_room(name="满员房间")
        room_id = result.data["room_id"]
        
        for i in range(2, 10):
            PlayerModel.create_player(
                f"{room_id}_user_{i}", room_id, f"user_{i}", seat=i, is_ai=False
            )
        PlayerModel.save_to_local()
        
        lobby2 = Lobby()
        lobby2.username = "join_full"
        result2 = lobby2.join_room(room_id=room_id)
        
        self.expect(result2.ok, False)
        self.expect("房间已满" in result2.title, True)
    
    def test_lobby_leave_room_success(self):
        lobby = Lobby()
        lobby.username = "leave_user"
        result = lobby.create_room(name="离开测试")
        room_id = result.data["room_id"]
        
        result2 = lobby.leave_room(room_id=room_id)
        
        self.expect(result2.ok, True)
        
        player = PlayerModel.get_player_by_room_username(room_id, "leave_user")
        self.expect(player is None, True)
        
        room_exists = RoomModel.exist(room_id)
        self.expect(room_exists, False)
    
    def test_lobby_leave_room_host_transfer(self):
        lobby1 = Lobby()
        lobby1.username = "host_transfer"
        result1 = lobby1.create_room(name="房主转移测试")
        room_id = result1.data["room_id"]
        
        lobby2 = Lobby()
        lobby2.username = "join_user_transfer"
        lobby2.join_room(room_id=room_id)
        
        lobby1.leave_room(room_id=room_id)
        
        room = RoomModel.get(room_id)
        self.expect(room.host.get_value(), "join_user_transfer")
    
    def test_lobby_add_ai_player_success(self):
        lobby = Lobby()
        lobby.username = "ai_host"
        result = lobby.create_room(name="AI测试")
        room_id = result.data["room_id"]
        
        result2 = lobby.add_ai_player(room_id=room_id)
        
        self.expect(result2.ok, True)
        self.expect("ai_username" in result2.data, True)
        
        ai_player = PlayerModel.get_player_by_room_username(room_id, result2.data["ai_username"])
        self.expect(ai_player.is_ai.get_value(), True)
        self.expect(ai_player.role.get_value(), Role.UNSET.value)
    
    def test_lobby_add_ai_not_host(self):
        lobby1 = Lobby()
        lobby1.username = "real_host"
        result1 = lobby1.create_room(name="AI非房主测试")
        room_id = result1.data["room_id"]
        
        lobby2 = Lobby()
        lobby2.username = "not_host"
        lobby2.join_room(room_id=room_id)
        
        result2 = lobby2.add_ai_player(room_id=room_id)
        
        self.expect(result2.ok, False)
        self.expect("只有房主" in result2.title, True)
    
    def test_lobby_set_ready_success(self):
        lobby = Lobby()
        lobby.username = "ready_user"
        result = lobby.create_room(name="准备测试")
        room_id = result.data["room_id"]
        
        result2 = lobby.set_ready(room_id=room_id, ready=True)
        
        self.expect(result2.ok, True)
        
        player = PlayerModel.get_player_by_room_username(room_id, "ready_user")
        self.expect(player.is_ready.get_value(), True)
        
        lobby.set_ready(room_id=room_id, ready=False)
        self.expect(player.is_ready.get_value(), False)
    
    def test_lobby_room_list_empty(self):
        lobby = Lobby()
        
        result = lobby.room_list()
        
        self.expect(result.ok, True)
        self.expect(len(result.data["rooms"]), 0)
    
    def test_lobby_room_list_with_rooms(self):
        lobby1 = Lobby()
        lobby1.username = "user_list_1"
        lobby1.create_room(name="房间A")
        
        lobby2 = Lobby()
        lobby2.username = "user_list_2"
        lobby2.create_room(name="房间B")
        
        lobby3 = Lobby()
        result = lobby3.room_list()
        
        self.expect(len(result.data["rooms"]), 2)
    
    def test_lobby_get_room_info_success(self):
        lobby = Lobby()
        lobby.username = "info_user"
        result = lobby.create_room(name="信息测试")
        room_id = result.data["room_id"]
        
        result2 = lobby.get_room_info(room_id=room_id)
        
        self.expect(result2.ok, True)
        self.expect("room" in result2.data, True)
        self.expect("players" in result2.data, True)
        self.expect(len(result2.data["players"]), 1)
        self.expect(result2.data["my_seat"], 1)


class TestLobbyWithStartedGame(TestBase):
    test_db_path = None
    
    @classmethod
    def setup_class(cls):
        cls.test_db_path = tempfile.mkdtemp(prefix="werewolf_lobby_game_test_")
        RoomModel.set_resource(os.path.join(cls.test_db_path, "room.db"))
        PlayerModel.set_resource(os.path.join(cls.test_db_path, "player.db"))
        RoomModel.init_resource()
        PlayerModel.init_resource()
    
    @classmethod
    def teardown_class(cls):
        if cls.test_db_path and os.path.exists(cls.test_db_path):
            import shutil
            shutil.rmtree(cls.test_db_path)
    
    def setup_method(self):
        RoomModel._config = {}
        RoomModel.instance_map = {}
        PlayerModel._config = {}
        PlayerModel.instance_map = {}
        for room in list(RoomModel.all()):
            room.delete()
        for player in list(PlayerModel.all()):
            player.delete()
        RoomModel.save_to_local()
        PlayerModel.save_to_local()
    
    def test_lobby_join_room_game_started(self):
        lobby = Lobby()
        lobby.username = "started_host"
        result = lobby.create_room(name="已开始游戏")
        room_id = result.data["room_id"]
        
        room = RoomModel.get(room_id)
        room.state.set_value(GameState.GAMING.value)
        RoomModel.save_to_local()
        
        lobby2 = Lobby()
        lobby2.username = "late_joiner"
        result2 = lobby2.join_room(room_id=room_id)
        
        self.expect(result2.ok, False)
        self.expect("游戏已开始" in result2.title, True)