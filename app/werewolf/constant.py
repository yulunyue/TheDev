from enum import Enum


class Role(str, Enum):
    UNSET = "unset"
    WOLF = "wolf"
    SEER = "seer"
    WITCH = "witch"
    GUARD = "guard"
    HUNTER = "hunter"
    VILLAGER = "villager"


class Phase(str, Enum):
    WAITING = "waiting"
    PREPARING = "preparing"
    NIGHT = "night"
    DAY = "day"
    VOTE = "vote"
    RESULT = "result"


class GameState(str, Enum):
    WAITING = "waiting"
    GAMING = "gaming"
    ENDED = "ended"


class Constant:
    TOPIC_WEREWOLF_LOBBY = "TOPIC_WEREWOLF_LOBBY"
    TOPIC_WEREWOLF_ROOM = "TOPIC_WEREWOLF_ROOM"
    
    MSG_ROOM_UPDATE = "room_update"
    MSG_GAME_START = "game_start"
    MSG_NIGHT_BEGIN = "night_begin"
    MSG_NIGHT_END = "night_end"
    MSG_DAY_BEGIN = "day_begin"
    MSG_DAY_END = "day_end"
    MSG_SPEECH = "speech"
    MSG_VOTE = "vote"
    MSG_VOTE_RESULT = "vote_result"
    MSG_DEATH = "death"
    MSG_GAME_END = "game_end"
    MSG_ROLE_INFO = "role_info"
    MSG_NIGHT_ACTION = "night_action"
    MSG_PLAYER_JOIN = "player_join"
    MSG_PLAYER_LEAVE = "player_leave"
    MSG_ERROR = "error"
    
    ROLE_CONFIG_9 = {
        Role.WOLF: 3,
        Role.SEER: 1,
        Role.WITCH: 1,
        Role.GUARD: 1,
        Role.HUNTER: 1,
        Role.VILLAGER: 2,
    }
    
    TOTAL_PLAYERS = 9
    MIN_HUMAN_PLAYERS = 1
    
    SPEECH_TIME_LIMIT = 60
    VOTE_TIME_LIMIT = 30
    NIGHT_ACTION_TIME_LIMIT = 20
    
    AI_NAME_PREFIX = "AI_"


C = Constant()