from common.util.export import IO_MANAGE, Node, json, random, time, logger
from .models import RoomModel, PlayerModel, GameLogModel, AIMemoryModel
from .constant import Role, Phase, GameState, C


class GameEngine:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.room = RoomModel.get(room_id)
    
    @staticmethod
    def get_confirmed_roles(room_id: str, room, player, players: list) -> dict:
        if not player:
            return {}
        
        confirmed = {}
        
        if room.state.get_value() == GameState.ENDED.value:
            for p in players:
                role = p.role.get_value()
                if role and role != Role.UNSET.value:
                    confirmed[p.seat.get_value()] = role
            return confirmed
        
        my_role = player.role.get_value()
        if my_role and my_role != Role.UNSET.value:
            confirmed[player.seat.get_value()] = my_role
        
        if my_role == Role.WOLF.value:
            for p in players:
                if p.role.get_value() == Role.WOLF.value and p.username.get_value() != player.username.get_value():
                    confirmed[p.seat.get_value()] = Role.WOLF.value
        
        hunter_logs = GameLogModel.get_logs_by_room(room_id)
        for log in hunter_logs:
            if log.event_type.get_value() == "hunter_shot":
                actor_seat = int(log.actor.get_value())
                confirmed[actor_seat] = Role.HUNTER.value
        
        return confirmed
    
    def start_game(self):
        players = PlayerModel.get_players_by_room(self.room_id)
        
        roles = []
        for role_str, count in C.ROLE_CONFIG_9.items():
            role_enum = Role(role_str) if isinstance(role_str, str) else role_str
            roles.extend([role_enum.value] * count)
        
        random.shuffle(roles)
        
        for i, player in enumerate(sorted(players, key=lambda p: p.seat.get_value())):
            player.role.set_value(roles[i])
            player.is_alive.set_value(True)
            player.is_ready.set_value(False)
        PlayerModel.save_to_local()
        
        self.room.state.set_value(GameState.GAMING.value)
        self.room.phase.set_value(Phase.NIGHT.value)
        self.room.round_num.set_value(1)
        self.room.night_actions.set_value({})
        RoomModel.save_to_local()
        
        for player in players:
            self._send_role_info(player)
        
        self._broadcast_room(C.MSG_GAME_START, {"round": 1})
        
        wolves = [p for p in players if p.role.get_value() == Role.WOLF.value]
        for wolf in wolves:
            wolf_ids = [w.username.get_value() for w in wolves if w.username.get_value() != wolf.username.get_value()]
            AIMemoryModel.add_memory(
                self.room_id, wolf.username.get_value(), 1,
                "observation", json.dumps({"wolf_ids": wolf_ids, "type": "wolf_identity"})
            )
        
        self._broadcast_room(C.MSG_NIGHT_BEGIN, {"round": 1})
        
        self._process_ai_night_actions()
        
        logger.info(f"Game started in room {self.room_id}")
    
    def next_speaker(self):
        current = self.room.current_speaker.get_value()
        players = PlayerModel.get_players_by_room(self.room_id)
        alive_players = sorted([p for p in players if p.is_alive.get_value()], 
                               key=lambda p: p.seat.get_value())
        
        next_seat = current + 1
        found = False
        for p in alive_players:
            if p.seat.get_value() >= next_seat:
                next_seat = p.seat.get_value()
                found = True
                break
        
        if not found:
            self.room.phase.set_value(Phase.VOTE.value)
            self.room.current_speaker.set_value(0)
            RoomModel.save_to_local()
            
            self._broadcast_room(C.MSG_DAY_END, {})
            self._broadcast_room(C.MSG_VOTE, {"phase": "vote_start"})
            
            self._process_ai_votes()
        else:
            self.room.current_speaker.set_value(next_seat)
            RoomModel.save_to_local()
            
            next_player = PlayerModel.get_player_by_room_seat(self.room_id, next_seat)
            if next_player and next_player.is_ai.get_value():
                self._ai_speech(next_player)
    
    def process_vote(self, voter_seat: int, target_seat: int):
        night_actions = self.room.night_actions.get_value() or {}
        votes = night_actions.get("votes", {})
        votes[str(voter_seat)] = target_seat
        night_actions["votes"] = votes
        self.room.night_actions.set_value(night_actions)
        RoomModel.save_to_local()
        
        players = PlayerModel.get_players_by_room(self.room_id)
        alive_count = len([p for p in players if p.is_alive.get_value()])
        
        if len(votes) >= alive_count:
            self._end_vote()
    
    def _process_ai_votes(self):
        players = PlayerModel.get_players_by_room(self.room_id)
        ai_players = [p for p in players if p.is_ai.get_value() and p.is_alive.get_value()]
        
        for ai in ai_players:
            target = self._ai_vote_decision(ai)
            self.process_vote(ai.seat.get_value(), target)
    
    def _end_vote(self):
        night_actions = self.room.night_actions.get_value() or {}
        votes = night_actions.get("votes", {})
        
        vote_counts = {}
        for voter, target in votes.items():
            vote_counts[target] = vote_counts.get(target, 0) + 1
        
        max_votes = 0
        max_seat = 0
        tie = False
        for seat, count in vote_counts.items():
            if count > max_votes:
                max_votes = count
                max_seat = int(seat)
                tie = False
            elif count == max_votes:
                tie = True
        
        if tie or max_votes < len(votes) // 2 + 1:
            self._broadcast_room(C.MSG_VOTE_RESULT, {"tie": True, "votes": vote_counts})
            self._broadcast_room(C.MSG_DAY_END, {"no_death": True})
        else:
            target_player = PlayerModel.get_player_by_room_seat(self.room_id, max_seat)
            if target_player:
                self._kill_player(max_seat, "vote")
                self._broadcast_room(C.MSG_VOTE_RESULT, 
                    {"tie": False, "votes": vote_counts, "dead_seat": max_seat})
        
        self.room.night_actions.set_value({})
        RoomModel.save_to_local()
        
        if self._check_game_end():
            return
        
        self.room.phase.set_value(Phase.NIGHT.value)
        self.room.round_num.set_value(self.room.round_num.get_value() + 1)
        self.room.current_speaker.set_value(0)
        RoomModel.save_to_local()
        
        self._broadcast_room(C.MSG_NIGHT_BEGIN, {"round": self.room.round_num.get_value()})
        
        self._process_ai_night_actions()
    
    def night_action(self, actor_seat: int, role: str, action_type: str, target_seat: int):
        night_actions = self.room.night_actions.get_value() or {}
        
        if role == Role.WOLF.value:
            if action_type == "kill":
                wolf_actions = night_actions.get("wolf_kill", [])
                wolf_actions.append({"actor": actor_seat, "target": target_seat})
                night_actions["wolf_kill"] = wolf_actions
        
        elif role == Role.SEER.value:
            if action_type == "check":
                target_player = PlayerModel.get_player_by_room_seat(self.room_id, target_seat)
                if not target_player:
                    return {"ok": False, "title": "目标玩家不存在"}
                
                target_role = target_player.role.get_value()
                is_wolf = target_role == Role.WOLF.value
                
                night_actions["seer_check"] = {"actor": actor_seat, "target": target_seat, "is_wolf": is_wolf}
                
                actor_player = PlayerModel.get_player_by_room_seat(self.room_id, actor_seat)
                if actor_player:
                    AIMemoryModel.add_memory(
                        self.room_id, actor_player.username.get_value(), 
                        self.room.round_num.get_value(),
                        "observation", json.dumps({
                            "check_target": target_seat, 
                            "is_wolf": is_wolf, 
                            "type": "seer_check"
                        })
                    )
        
        elif role == Role.WITCH.value:
            if action_type == "save":
                wolf_actions = night_actions.get("wolf_kill", [])
                if wolf_actions:
                    last_kill = wolf_actions[-1]
                    if last_kill.get("target") == target_seat:
                        night_actions["witch_save"] = {"actor": actor_seat, "target": target_seat}
            elif action_type == "poison":
                if "witch_poison" not in night_actions:
                    night_actions["witch_poison"] = {"actor": actor_seat, "target": target_seat}
        
        elif role == Role.GUARD.value:
            if action_type == "protect":
                last_protected = night_actions.get("last_protected", 0)
                if target_seat != last_protected:
                    night_actions["guard_protect"] = {"actor": actor_seat, "target": target_seat}
        
        self.room.night_actions.set_value(night_actions)
        RoomModel.save_to_local()
        
        return {"ok": True}
    
    def hunter_shot(self, hunter_seat: int, target_seat: int):
        self._kill_player(target_seat, "hunter")
        
        GameLogModel.log_event(
            room_id=self.room_id,
            round_num=self.room.round_num.get_value(),
            phase=self.room.phase.get_value(),
            event_type="hunter_shot",
            actor=str(hunter_seat),
            target=str(target_seat),
            content=f"猎人{hunter_seat}号开枪射杀{target_seat}号",
        )
        
        self._check_game_end()
    
    def _process_ai_night_actions(self):
        players = PlayerModel.get_players_by_room(self.room_id)
        ai_players = [p for p in players if p.is_ai.get_value() and p.is_alive.get_value()]
        
        wolves = [p for p in ai_players if p.role.get_value() == Role.WOLF.value]
        if wolves:
            target = self._ai_wolf_kill_decision(wolves)
            self.night_action(wolves[0].seat.get_value(), Role.WOLF.value, "kill", target)
        
        for ai in ai_players:
            role = ai.role.get_value()
            if role == Role.SEER.value:
                target = self._ai_seer_check_decision(ai)
                self.night_action(ai.seat.get_value(), Role.SEER.value, "check", target)
            elif role == Role.WITCH.value:
                action, target = self._ai_witch_decision(ai)
                if action:
                    self.night_action(ai.seat.get_value(), Role.WITCH.value, action, target)
            elif role == Role.GUARD.value:
                target = self._ai_guard_decision(ai)
                if target:
                    self.night_action(ai.seat.get_value(), Role.GUARD.value, "protect", target)
        
        night_actions = self.room.night_actions.get_value() or {}
        night_actions["ai_done"] = True
        self.room.night_actions.set_value(night_actions)
        RoomModel.save_to_local()
        
        self._check_night_complete()
    
    def finish_night_action(self, username: str):
        night_actions = self.room.night_actions.get_value() or {}
        done_players = night_actions.get("human_done", [])
        if username not in done_players:
            done_players.append(username)
        night_actions["human_done"] = done_players
        self.room.night_actions.set_value(night_actions)
        RoomModel.save_to_local()
        
        self._check_night_complete()
    
    def _check_night_complete(self):
        players = PlayerModel.get_players_by_room(self.room_id)
        human_players = [p for p in players if not p.is_ai.get_value() and p.is_alive.get_value()]
        
        night_actions = self.room.night_actions.get_value() or {}
        human_done = night_actions.get("human_done", [])
        ai_done = night_actions.get("ai_done", False)
        
        all_human_done = len(human_done) >= len(human_players)
        
        if all_human_done and ai_done:
            self._end_night()
    
    def _end_night(self):
        night_actions = self.room.night_actions.get_value() or {}
        
        deaths = []
        
        wolf_kill_target = 0
        wolf_actions = night_actions.get("wolf_kill", [])
        if wolf_actions:
            wolf_kill_target = wolf_actions[-1].get("target", 0)
        
        saved = False
        if night_actions.get("witch_save"):
            saved = True
        
        protected = False
        if night_actions.get("guard_protect"):
            guard_action = night_actions.get("guard_protect")
            if guard_action.get("target") == wolf_kill_target:
                protected = True
            night_actions["last_protected"] = guard_action.get("target")
        
        if wolf_kill_target > 0 and not saved and not protected:
            deaths.append(wolf_kill_target)
        
        if night_actions.get("witch_poison"):
            poison_target = night_actions.get("witch_poison").get("target", 0)
            if poison_target > 0:
                deaths.append(poison_target)
        
        for seat in deaths:
            self._kill_player(seat, "night")
        
        self.room.night_actions.set_value(night_actions)
        RoomModel.save_to_local()
        
        if self._check_game_end():
            return
        
        self.room.phase.set_value(Phase.DAY.value)
        self.room.current_speaker.set_value(1)
        self.room.day_time.set_value(int(time.time() * 1000))
        RoomModel.save_to_local()
        
        self._broadcast_room(C.MSG_NIGHT_END, {"deaths": deaths})
        self._broadcast_room(C.MSG_DAY_BEGIN, {"round": self.room.round_num.get_value()})
        
        first_speaker = PlayerModel.get_player_by_room_seat(self.room_id, 1)
        if first_speaker and first_speaker.is_alive.get_value() and first_speaker.is_ai.get_value():
            self._ai_speech(first_speaker)
    
    def _kill_player(self, seat: int, reason: str):
        player = PlayerModel.get_player_by_room_seat(self.room_id, seat)
        if player:
            player.is_alive.set_value(False)
            PlayerModel.save_to_local()
            
            self._broadcast_room(C.MSG_DEATH, {"seat": seat, "reason": reason, "username": player.username.get_value()})
            
            if player.role.get_value() == Role.HUNTER.value and reason != "hunter":
                self._broadcast_room(C.MSG_NIGHT_ACTION, {"type": "hunter_can_shot", "seat": seat})
    
    def _check_game_end(self):
        players = PlayerModel.get_players_by_room(self.room_id)
        alive_players = [p for p in players if p.is_alive.get_value()]
        
        alive_wolves = [p for p in alive_players if p.role.get_value() == Role.WOLF.value]
        alive_good = [p for p in alive_players if p.role.get_value() not in (Role.WOLF.value, Role.UNSET.value)]
        
        if len(alive_wolves) == 0:
            self._end_game("good_win")
            return True
        
        if len(alive_wolves) >= len(alive_good):
            self._end_game("wolf_win")
            return True
        
        return False
    
    def _end_game(self, result: str):
        self.room.state.set_value(GameState.ENDED.value)
        self.room.phase.set_value(Phase.RESULT.value)
        RoomModel.save_to_local()
        
        players = PlayerModel.get_players_by_room(self.room_id)
        player_info = [{"seat": p.seat.get_value(), "username": p.username.get_value(), 
                        "role": p.role.get_value(), "is_ai": p.is_ai.get_value()} for p in players]
        
        self._broadcast_room(C.MSG_GAME_END, {"result": result, "players": player_info})
        
        logger.info(f"Game ended in room {self.room_id}, result: {result}")
    
    def _send_role_info(self, player: PlayerModel):
        topic = f"{C.TOPIC_WEREWOLF_ROOM}_{self.room_id}_{player.username.get_value()}"
        
        wolves = []
        if player.role.get_value() == Role.WOLF.value:
            all_players = PlayerModel.get_players_by_room(self.room_id)
            wolves = [p.seat.get_value() for p in all_players 
                      if p.role.get_value() == Role.WOLF.value and p.username.get_value() != player.username.get_value()]
        
        IO_MANAGE.send(topic, {
            "type": C.MSG_ROLE_INFO,
            "role": player.role.get_value(),
            "seat": player.seat.get_value(),
            "wolves": wolves,
        })
    
    def _broadcast_room(self, msg_type: str, data: dict):
        topic = f"{C.TOPIC_WEREWOLF_ROOM}_{self.room_id}"
        IO_MANAGE.send(topic, {"type": msg_type, **data})
    
    def _ai_speech(self, ai_player: PlayerModel):
        speeches = [
            "我觉得这局情况比较复杂，大家发言都比较谨慎。",
            "我观察到有些玩家的发言逻辑有问题，需要进一步分析。",
            "我认为我们应该仔细分析昨夜的死亡情况。",
            "从发言来看，有人可能在刻意隐藏身份。",
            "我暂时不发表具体怀疑对象，先听听其他人的分析。",
        ]
        
        role_speeches = {
            Role.WOLF.value: [
                "我认为我们应该仔细分析发言，找出逻辑漏洞。",
                "昨夜的死亡很蹊跷，我们需要认真思考。",
                "我怀疑某些人的发言过于激进。",
                "我们应该团结起来，找出可疑的人。",
                "从我的观察来看，某些人行为异常。",
            ],
            Role.SEER.value: [
                "我有重要信息要分享，但现在还不是时候。",
                "我建议大家仔细分析发言逻辑。",
                "某些发言让我产生了怀疑。",
                "我们需要更多的信息来判断。",
                "我会根据后续发言来决定是否公开信息。",
            ],
        }
        
        role = ai_player.role.get_value()
        if role in role_speeches:
            content = random.choice(role_speeches[role])
        else:
            content = random.choice(speeches)
        
        GameLogModel.log_event(
            room_id=self.room_id,
            round_num=self.room.round_num.get_value(),
            phase=Phase.DAY.value,
            event_type=C.MSG_SPEECH,
            actor=ai_player.username.get_value(),
            content=content,
        )
        
        self._broadcast_room(C.MSG_SPEECH, {
            "seat": ai_player.seat.get_value(),
            "username": ai_player.username.get_value(),
            "content": content,
        })
        
        self.next_speaker()
    
    def _ai_vote_decision(self, ai_player: PlayerModel) -> int:
        players = PlayerModel.get_players_by_room(self.room_id)
        alive_players = [p for p in players if p.is_alive.get_value() and p.username.get_value() != ai_player.username.get_value()]
        
        if ai_player.role.get_value() == Role.WOLF.value:
            for p in alive_players:
                if p.role.get_value() == Role.SEER.value:
                    return p.seat.get_value()
        
        return random.choice(alive_players).seat.get_value()
    
    def _ai_wolf_kill_decision(self, wolves: list) -> int:
        players = PlayerModel.get_players_by_room(self.room_id)
        targets = [p for p in players if p.is_alive.get_value() and p.role.get_value() not in (Role.WOLF.value, Role.UNSET.value)]
        
        for t in targets:
            if t.role.get_value() == Role.SEER.value:
                return t.seat.get_value()
        
        return random.choice(targets).seat.get_value()
    
    def _ai_seer_check_decision(self, ai_player: PlayerModel) -> int:
        players = PlayerModel.get_players_by_room(self.room_id)
        targets = [p for p in players if p.is_alive.get_value() and p.username.get_value() != ai_player.username.get_value()]
        return random.choice(targets).seat.get_value()
    
    def _ai_witch_decision(self, ai_player: PlayerModel) -> tuple:
        night_actions = self.room.night_actions.get_value() or {}
        wolf_kill = night_actions.get("wolf_kill", [])
        
        if wolf_kill:
            kill_target = wolf_kill[-1].get("target", 0)
            if kill_target and not night_actions.get("witch_save"):
                return ("save", kill_target)
        
        return (None, 0)
    
    def _ai_guard_decision(self, ai_player: PlayerModel) -> int:
        night_actions = self.room.night_actions.get_value() or {}
        last_protected = night_actions.get("last_protected", 0)
        
        players = PlayerModel.get_players_by_room(self.room_id)
        targets = [p for p in players if p.is_alive.get_value() and p.seat.get_value() != last_protected]
        
        return random.choice(targets).seat.get_value()