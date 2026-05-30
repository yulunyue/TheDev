import os
import sys
import tempfile
from common.util.export import TestBase, assert_dict
from app.werewolf.model import RoomModel, PlayerModel, GameLogModel, AIMemoryModel
from app.werewolf.constant import Role, Phase, GameState


class TestRoomModel(TestBase):
    test_db_path = None
    
    @classmethod
    def setup_class(cls):
        cls.test_db_path = tempfile.mkdtemp(prefix="werewolf_test_")
        RoomModel.set_resource(os.path.join(cls.test_db_path, "room.db"))
        RoomModel.init_resource()
    
    @classmethod
    def teardown_class(cls):
        if hasattr(RoomModel, '_conn') and RoomModel._conn:
            RoomModel._conn.close()
        if cls.test_db_path and os.path.exists(cls.test_db_path):
            import shutil
            shutil.rmtree(cls.test_db_path)
    
    def setup_method(self):
        RoomModel._config = {}
        RoomModel.instance_map = {}
        for room in list(RoomModel.all()):
            room.delete()
        RoomModel.save_to_local()
    
    def test_room_create_success(self):
        room = RoomModel.create_room("test_room_1", "测试房间", "user1")
        self.expect(room._id, "test_room_1")
        self.expect(room.name.get_value(), "测试房间")
        self.expect(room.host.get_value(), "user1")
        self.expect(room.state.get_value(), GameState.WAITING.value)
        self.expect(room.phase.get_value(), Phase.WAITING.value)
    
    def test_room_to_public_dict(self):
        RoomModel.create_room("test_room_2", "公开信息测试", "user2")
        room = RoomModel.query("test_room_2")
        public_dict = room.to_public_dict()
        self.expect(public_dict["id"], "test_room_2")
        self.expect(public_dict["name"], "公开信息测试")
        self.expect(public_dict["host"], "user2")
        self.expect("config" not in public_dict, True)
    
    def test_room_phase_change(self):
        RoomModel.create_room("test_room_3", "阶段测试", "user3")
        room = RoomModel.query("test_room_3")
        room.phase.set_value(Phase.NIGHT.value)
        room.round_num.set_value(2)
        RoomModel.save_to_local()
        
        room2 = RoomModel.query("test_room_3")
        self.expect(room2.phase.get_value(), Phase.NIGHT.value)
        self.expect(room2.round_num.get_value(), 2)
    
    def test_room_delete(self):
        RoomModel.create_room("test_room_4", "删除测试", "user4")
        room = RoomModel.query("test_room_4")
        self.expect(room is not None, True)
        
        room.delete()
        RoomModel.save_to_local()
        
        rooms = list(RoomModel.all())
        self.expect(len(rooms), 0)


class TestPlayerModel(TestBase):
    test_db_path = None
    
    @classmethod
    def setup_class(cls):
        cls.test_db_path = tempfile.mkdtemp(prefix="werewolf_test_player_")
        PlayerModel.set_resource(os.path.join(cls.test_db_path, "player.db"))
        PlayerModel.init_resource()
    
    @classmethod
    def teardown_class(cls):
        if hasattr(PlayerModel, '_conn') and PlayerModel._conn:
            PlayerModel._conn.close()
        if cls.test_db_path and os.path.exists(cls.test_db_path):
            import shutil
            shutil.rmtree(cls.test_db_path)
    
    def setup_method(self):
        PlayerModel._config = {}
        PlayerModel.instance_map = {}
        for player in list(PlayerModel.all()):
            player.delete()
        PlayerModel.save_to_local()
    
    def test_player_create_human(self):
        player = PlayerModel.create_player(
            "room1_user1", "room1", "user1", seat=1, is_ai=False
        )
        self.expect(player._id, "room1_user1")
        self.expect(player.room_id.get_value(), "room1")
        self.expect(player.username.get_value(), "user1")
        self.expect(player.seat.get_value(), 1)
        self.expect(player.is_ai.get_value(), False)
        self.expect(player.is_alive.get_value(), True)
    
    def test_player_create_ai(self):
        player = PlayerModel.create_player(
            "room1_ai1", "room1", "AI_123_2", seat=2, is_ai=True, ai_persona="激进型"
        )
        self.expect(player.is_ai.get_value(), True)
        self.expect(player.ai_persona.get_value(), "激进型")
    
    def test_player_role_assignment(self):
        player = PlayerModel.create_player("room2_p1", "room2", "p1", seat=1)
        player.role.set_value(Role.WOLF.value)
        PlayerModel.save_to_local()
        
        p = PlayerModel.query("room2_p1")
        self.expect(p.role.get_value(), Role.WOLF.value)
    
    def test_player_alive_toggle(self):
        player = PlayerModel.create_player("room3_p1", "room3", "p1", seat=1)
        self.expect(player.is_alive.get_value(), True)
        
        player.is_alive.set_value(False)
        PlayerModel.save_to_local()
        
        p = PlayerModel.query("room3_p1")
        self.expect(p.is_alive.get_value(), False)
    
    def test_player_get_by_room_seat(self):
        PlayerModel.create_player("room4_p1", "room4", "p1", seat=1)
        PlayerModel.create_player("room4_p2", "room4", "p2", seat=2)
        PlayerModel.create_player("room4_p3", "room4", "p3", seat=3)
        
        player = PlayerModel.get_player_by_room_seat("room4", 2)
        self.expect(player.username.get_value(), "p2")
        
        player_none = PlayerModel.get_player_by_room_seat("room4", 99)
        self.expect(player_none is None, True)
    
    def test_player_get_by_room_username(self):
        PlayerModel.create_player("room5_p1", "room5", "user_a", seat=1)
        PlayerModel.create_player("room5_p2", "room5", "user_b", seat=2)
        
        player = PlayerModel.get_player_by_room_username("room5", "user_a")
        self.expect(player.seat.get_value(), 1)
        
        player_none = PlayerModel.get_player_by_room_username("room5", "user_c")
        self.expect(player_none is None, True)
    
    def test_player_get_players_by_room(self):
        PlayerModel.create_player("room6_p1", "room6", "p1", seat=1)
        PlayerModel.create_player("room6_p2", "room6", "p2", seat=2)
        PlayerModel.create_player("room6_p3", "room6", "p3", seat=3)
        PlayerModel.create_player("other_p", "other_room", "p4", seat=1)
        
        players = PlayerModel.get_players_by_room("room6")
        self.expect(len(players), 3)
    
    def test_player_to_public_dict(self):
        player = PlayerModel.create_player("room7_p1", "room7", "p1", seat=1)
        player.role.set_value(Role.SEER.value)
        PlayerModel.save_to_local()
        
        public_dict = player.to_public_dict()
        self.expect("role" not in public_dict, True)
        self.expect(public_dict["seat"], 1)
        self.expect(public_dict["username"], "p1")
    
    def test_player_to_private_dict(self):
        player = PlayerModel.create_player("room8_p1", "room8", "p1", seat=1)
        player.role.set_value(Role.SEER.value)
        PlayerModel.save_to_local()
        
        private_dict = player.to_private_dict()
        self.expect(private_dict["role"], Role.SEER.value)


class TestGameLogModel(TestBase):
    test_db_path = None
    
    @classmethod
    def setup_class(cls):
        cls.test_db_path = tempfile.mkdtemp(prefix="werewolf_test_log_")
        GameLogModel.set_resource(os.path.join(cls.test_db_path, "game_log.db"))
        GameLogModel.init_resource()
    
    @classmethod
    def teardown_class(cls):
        if hasattr(GameLogModel, '_conn') and GameLogModel._conn:
            GameLogModel._conn.close()
        if cls.test_db_path and os.path.exists(cls.test_db_path):
            import shutil
            shutil.rmtree(cls.test_db_path)
    
    def setup_method(self):
        GameLogModel._config = {}
        GameLogModel.instance_map = {}
        for log in list(GameLogModel.all()):
            log.delete()
        GameLogModel.save_to_local()
    
    def test_log_event_create(self):
        log = GameLogModel.log_event(
            room_id="room1",
            round_num=1,
            phase="night",
            event_type="speech",
            actor="user1",
            target="2",
            content="我怀疑2号是狼"
        )
        self.expect(log.room_id.get_value(), "room1")
        self.expect(log.round_num.get_value(), 1)
        self.expect(log.event_type.get_value(), "speech")
        self.expect(log.actor.get_value(), "user1")
        self.expect(log.content.get_value(), "我怀疑2号是狼")
    
    def test_log_get_by_room(self):
        GameLogModel.log_event("room2", 1, "day", "speech", "u1", "", "发言1")
        GameLogModel.log_event("room2", 1, "day", "vote", "u1", "2", "投票")
        GameLogModel.log_event("room2", 2, "night", "kill", "wolf", "3", "杀人")
        GameLogModel.log_event("room3", 1, "day", "speech", "u2", "", "发言2")
        
        logs_room2 = GameLogModel.get_logs_by_room("room2")
        self.expect(len(logs_room2), 3)
        
        logs_room2_r1 = GameLogModel.get_logs_by_room("room2", round_num=1)
        self.expect(len(logs_room2_r1), 2)
    
    def test_log_order_by_timestamp(self):
        import time
        GameLogModel.log_event("room4", 1, "day", "speech", "u1", "", "第一")
        time.sleep(0.01)
        GameLogModel.log_event("room4", 1, "day", "speech", "u2", "", "第二")
        time.sleep(0.01)
        GameLogModel.log_event("room4", 1, "day", "speech", "u3", "", "第三")
        
        logs = GameLogModel.get_logs_by_room("room4")
        self.expect(logs[0].actor.get_value(), "u1")
        self.expect(logs[2].actor.get_value(), "u3")


class TestAIMemoryModel(TestBase):
    test_db_path = None
    
    @classmethod
    def setup_class(cls):
        cls.test_db_path = tempfile.mkdtemp(prefix="werewolf_test_memory_")
        AIMemoryModel.set_resource(os.path.join(cls.test_db_path, "ai_memory.db"))
        AIMemoryModel.init_resource()
    
    @classmethod
    def teardown_class(cls):
        if hasattr(AIMemoryModel, '_conn') and AIMemoryModel._conn:
            AIMemoryModel._conn.close()
        if cls.test_db_path and os.path.exists(cls.test_db_path):
            import shutil
            shutil.rmtree(cls.test_db_path)
    
    def setup_method(self):
        AIMemoryModel._config = {}
        AIMemoryModel.instance_map = {}
        for mem in list(AIMemoryModel.all()):
            mem.delete()
        AIMemoryModel.save_to_local()
    
    def test_memory_add(self):
        mem = AIMemoryModel.add_memory(
            room_id="room1",
            player_id="ai_player_1",
            round_num=1,
            memory_type="observation",
            content='{"check_target": 2, "is_wolf": true}'
        )
        self.expect(mem.room_id.get_value(), "room1")
        self.expect(mem.player_id.get_value(), "ai_player_1")
        self.expect(mem.memory_type.get_value(), "observation")
    
    def test_memory_get_by_player(self):
        AIMemoryModel.add_memory("room2", "ai1", 1, "obs1", '{"data": 1}')
        AIMemoryModel.add_memory("room2", "ai1", 2, "obs2", '{"data": 2}')
        AIMemoryModel.add_memory("room2", "ai2", 1, "obs3", '{"data": 3}')
        
        memories = AIMemoryModel.get_memories("room2", "ai1")
        self.expect(len(memories), 2)
        
        memories_r1 = AIMemoryModel.get_memories("room2", "ai1", round_num=1)
        self.expect(len(memories_r1), 1)
    
    def test_memory_order_by_timestamp(self):
        import time
        AIMemoryModel.add_memory("room3", "ai1", 1, "obs", '{"a": 1}')
        time.sleep(0.01)
        AIMemoryModel.add_memory("room3", "ai1", 1, "obs", '{"b": 2}')
        
        memories = AIMemoryModel.get_memories("room3", "ai1")
        self.expect(memories[0].content.get_value(), '{"a": 1}')