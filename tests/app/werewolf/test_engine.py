import os
import sys
import tempfile
from common.util.export import TestBase, assert_dict, json, random
from app.werewolf.model import RoomModel, PlayerModel, GameLogModel
from app.werewolf.constant import Role, Phase, GameState, C
from app.werewolf.engine import GameEngine


class TestGameEngine(TestBase):
    test_db_path = None
    
    @classmethod
    def setup_class(cls):
        cls.test_db_path = tempfile.mkdtemp(prefix="werewolf_engine_test_")
        RoomModel.set_resource(os.path.join(cls.test_db_path, "room.db"))
        PlayerModel.set_resource(os.path.join(cls.test_db_path, "player.db"))
        GameLogModel.set_resource(os.path.join(cls.test_db_path, "game_log.db"))
        RoomModel.init_resource()
        PlayerModel.init_resource()
        GameLogModel.init_resource()
    
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
        GameLogModel._config = {}
        GameLogModel.instance_map = {}
        for room in list(RoomModel.all()):
            room.delete()
        for player in list(PlayerModel.all()):
            player.delete()
        for log in list(GameLogModel.all()):
            log.delete()
        RoomModel.save_to_local()
        PlayerModel.save_to_local()
        GameLogModel.save_to_local()
    
    def _create_full_room(self, room_id: str, host: str = "host") -> str:
        RoomModel.create_room(room_id, "测试房间", host)
        
        PlayerModel.create_player(f"{room_id}_{host}", room_id, host, seat=1, is_ai=False)
        for i in range(2, 10):
            PlayerModel.create_player(
                f"{room_id}_player_{i}", room_id, f"player_{i}", seat=i, is_ai=True
            )
        PlayerModel.save_to_local()
        return room_id
    
    def test_start_game_role_assignment(self):
        room_id = self._create_full_room("test_role_assign")
        
        engine = GameEngine(room_id)
        engine.start_game()
        
        players = PlayerModel.get_players_by_room(room_id)
        
        role_counts = {}
        for p in players:
            role = p.role.get_value()
            role_counts[role] = role_counts.get(role, 0) + 1
        
        self.expect(role_counts.get(Role.WOLF.value, 0), 3)
        self.expect(role_counts.get(Role.SEER.value, 0), 1)
        self.expect(role_counts.get(Role.WITCH.value, 0), 1)
        self.expect(role_counts.get(Role.GUARD.value, 0), 1)
        self.expect(role_counts.get(Role.HUNTER.value, 0), 1)
        self.expect(role_counts.get(Role.VILLAGER.value, 0), 2)
        self.expect(Role.UNSET.value not in role_counts, True)
    
    def test_start_game_state_change(self):
        room_id = self._create_full_room("test_state_change")
        
        engine = GameEngine(room_id)
        engine.start_game()
        
        room = RoomModel.get(room_id)
        self.expect(room.state.get_value(), GameState.GAMING.value)
        self.expect(room.phase.get_value(), Phase.NIGHT.value)
        self.expect(room.round_num.get_value(), 1)
    
    def test_start_game_unset_players_excluded(self):
        room_id = "test_unset_exclude"
        RoomModel.create_room(room_id, "测试房间", "host")
        
        for i in range(1, 10):
            PlayerModel.create_player(
                f"{room_id}_player_{i}", room_id, f"player_{i}", seat=i, is_ai=True
            )
        PlayerModel.save_to_local()
        
        player_1 = PlayerModel.get_player_by_room_seat(room_id, 1)
        player_1.role.set_value(Role.UNSET.value)
        player_1.is_alive.set_value(True)
        PlayerModel.save_to_local()
        
        engine = GameEngine(room_id)
        
        player_1.role.set_value(Role.WOLF.value)
        PlayerModel.save_to_local()
        
        wolves = [p for p in PlayerModel.get_players_by_room(room_id) if p.role.get_value() == Role.WOLF.value]
        self.expect(len(wolves) > 0, True)
    
    def test_night_action_wolf_kill(self):
        room_id = self._create_full_room("test_wolf_kill")
        engine = GameEngine(room_id)
        engine.start_game()
        
        wolves = [p for p in PlayerModel.get_players_by_room(room_id) if p.role.get_value() == Role.WOLF.value]
        wolf_seat = wolves[0].seat.get_value()
        
        engine.night_action(wolf_seat, Role.WOLF.value, "kill", 5)
        
        room = RoomModel.get(room_id)
        night_actions = room.night_actions.get_value()
        self.expect("wolf_kill" in night_actions, True)
        self.expect(night_actions["wolf_kill"][0]["target"], 5)
    
    def test_night_action_seer_check_wolf(self):
        room_id = self._create_full_room("test_seer_check")
        engine = GameEngine(room_id)
        engine.start_game()
        
        seer = [p for p in PlayerModel.get_players_by_room(room_id) if p.role.get_value() == Role.SEER.value][0]
        wolves = [p for p in PlayerModel.get_players_by_room(room_id) if p.role.get_value() == Role.WOLF.value]
        wolf_seat = wolves[0].seat.get_value()
        
        result = engine.night_action(seer.seat.get_value(), Role.SEER.value, "check", wolf_seat)
        
        self.expect(result["ok"], True)
        
        room = RoomModel.get(room_id)
        night_actions = room.night_actions.get_value()
        self.expect("seer_check" in night_actions, True)
        self.expect(night_actions["seer_check"]["is_wolf"], True)
    
    def test_night_action_seer_check_good(self):
        room_id = self._create_full_room("test_seer_good")
        engine = GameEngine(room_id)
        engine.start_game()
        
        seer = [p for p in PlayerModel.get_players_by_room(room_id) if p.role.get_value() == Role.SEER.value][0]
        villagers = [p for p in PlayerModel.get_players_by_room(room_id) if p.role.get_value() == Role.VILLAGER.value]
        target_seat = villagers[0].seat.get_value()
        
        result = engine.night_action(seer.seat.get_value(), Role.SEER.value, "check", target_seat)
        
        self.expect(result["ok"], True)
        
        room = RoomModel.get(room_id)
        night_actions = room.night_actions.get_value()
        self.expect(night_actions["seer_check"]["is_wolf"], False)
    
    def test_night_action_witch_save(self):
        room_id = self._create_full_room("test_witch_save")
        engine = GameEngine(room_id)
        engine.start_game()
        
        wolves = [p for p in PlayerModel.get_players_by_room(room_id) if p.role.get_value() == Role.WOLF.value]
        witch = [p for p in PlayerModel.get_players_by_room(room_id) if p.role.get_value() == Role.WITCH.value][0]
        
        target_seat = 5
        engine.night_action(wolves[0].seat.get_value(), Role.WOLF.value, "kill", target_seat)
        
        engine.night_action(witch.seat.get_value(), Role.WITCH.value, "save", target_seat)
        
        room = RoomModel.get(room_id)
        night_actions = room.night_actions.get_value()
        self.expect("witch_save" in night_actions, True)
    
    def test_night_action_guard_protect(self):
        room_id = self._create_full_room("test_guard")
        engine = GameEngine(room_id)
        engine.start_game()
        
        guard = [p for p in PlayerModel.get_players_by_room(room_id) if p.role.get_value() == Role.GUARD.value][0]
        
        engine.night_action(guard.seat.get_value(), Role.GUARD.value, "protect", 5)
        
        room = RoomModel.get(room_id)
        night_actions = room.night_actions.get_value()
        self.expect("guard_protect" in night_actions, True)
        self.expect(night_actions["guard_protect"]["target"], 5)
    
    def test_kill_player_success(self):
        room_id = self._create_full_room("test_kill")
        engine = GameEngine(room_id)
        engine.start_game()
        
        engine._kill_player(5, "night")
        
        player = PlayerModel.get_player_by_room_seat(room_id, 5)
        self.expect(player.is_alive.get_value(), False)
    
    def test_check_game_end_good_win(self):
        room_id = self._create_full_room("test_good_win")
        engine = GameEngine(room_id)
        engine.start_game()
        
        wolves = [p for p in PlayerModel.get_players_by_room(room_id) if p.role.get_value() == Role.WOLF.value]
        for w in wolves:
            w.is_alive.set_value(False)
        PlayerModel.save_to_local()
        
        result = engine._check_game_end()
        
        self.expect(result, True)
        
        room = RoomModel.get(room_id)
        self.expect(room.state.get_value(), GameState.ENDED.value)
    
    def test_check_game_end_wolf_win(self):
        room_id = self._create_full_room("test_wolf_win")
        engine = GameEngine(room_id)
        engine.start_game()
        
        players = PlayerModel.get_players_by_room(room_id)
        alive_count = 0
        for p in players:
            if p.role.get_value() == Role.WOLF.value:
                p.is_alive.set_value(True)
                alive_count += 1
            else:
                p.is_alive.set_value(False)
        PlayerModel.save_to_local()
        
        result = engine._check_game_end()
        
        self.expect(result, True)
        
        room = RoomModel.get(room_id)
        self.expect(room.state.get_value(), GameState.ENDED.value)
    
    def test_check_game_end_unset_excluded(self):
        room_id = self._create_full_room("test_unset_game")
        engine = GameEngine(room_id)
        engine.start_game()
        
        for p in PlayerModel.get_players_by_room(room_id):
            if p.role.get_value() != Role.WOLF.value:
                p.is_alive.set_value(False)
            else:
                p.is_alive.set_value(True)
        
        unset_player = PlayerModel.get_player_by_room_seat(room_id, 1)
        unset_player.role.set_value(Role.UNSET.value)
        unset_player.is_alive.set_value(True)
        PlayerModel.save_to_local()
        
        result = engine._check_game_end()
        
        self.expect(result, True)
    
    def test_ai_wolf_kill_exclude_unset(self):
        room_id = self._create_full_room("test_ai_wolf")
        engine = GameEngine(room_id)
        engine.start_game()
        
        wolves = [p for p in PlayerModel.get_players_by_room(room_id) if p.role.get_value() == Role.WOLF.value]
        
        for p in PlayerModel.get_players_by_room(room_id):
            if p.role.get_value() == Role.UNSET.value:
                p.is_alive.set_value(True)
        
        target = engine._ai_wolf_kill_decision(wolves)
        
        target_player = PlayerModel.get_player_by_room_seat(room_id, target)
        self.expect(target_player.role.get_value() != Role.WOLF.value, True)
        self.expect(target_player.role.get_value() != Role.UNSET.value, True)


class TestRoleUnset(TestBase):
    test_db_path = None
    
    @classmethod
    def setup_class(cls):
        cls.test_db_path = tempfile.mkdtemp(prefix="werewolf_unset_test_")
        PlayerModel.set_resource(os.path.join(cls.test_db_path, "player.db"))
        PlayerModel.init_resource()
    
    @classmethod
    def teardown_class(cls):
        if cls.test_db_path and os.path.exists(cls.test_db_path):
            import shutil
            shutil.rmtree(cls.test_db_path)
    
    def setup_method(self):
        PlayerModel._config = {}
        PlayerModel.instance_map = {}
        for player in list(PlayerModel.all()):
            player.delete()
        PlayerModel.save_to_local()
    
    def test_player_create_role_unset(self):
        player = PlayerModel.create_player("unset_test_1", "room_1", "user_1", seat=1, is_ai=False)
        
        self.expect(player.role.get_value(), Role.UNSET.value)
    
    def test_unset_value_valid_for_select_model(self):
        player = PlayerModel.create_player("unset_test_2", "room_2", "user_2", seat=2, is_ai=False)
        
        self.expect(player.role.get_value(), Role.UNSET.value)
        
        player.role.set_value(Role.WOLF.value)
        PlayerModel.save_to_local()
        
        p = PlayerModel.query("unset_test_2")
        self.expect(p.role.get_value(), Role.WOLF.value)
    
    def test_unset_to_wolf_assignment(self):
        player = PlayerModel.create_player("unset_test_3", "room_3", "user_3", seat=3, is_ai=False)
        
        self.expect(player.role.get_value(), Role.UNSET.value)
        
        player.role.set_value(Role.WOLF.value)
        PlayerModel.save_to_local()
        
        p = PlayerModel.query("unset_test_3")
        self.expect(p.role.get_value(), Role.WOLF.value)
    
    def test_unset_not_in_game_roles(self):
        game_roles = [Role.WOLF, Role.SEER, Role.WITCH, Role.GUARD, Role.HUNTER, Role.VILLAGER]
        
        self.expect(Role.UNSET not in game_roles, True)
    
    def test_unset_excluded_from_role_config(self):
        config_roles = list(C.ROLE_CONFIG_9.keys())
        
        unset_in_config = False
        for role in config_roles:
            if isinstance(role, str) and role == Role.UNSET.value:
                unset_in_config = True
            elif hasattr(role, 'value') and role.value == Role.UNSET.value:
                unset_in_config = True
        
        self.expect(unset_in_config, False)