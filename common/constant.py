class Constant:
    APP_NAME = "TheDev"
    CODE_500 = 500
    CODE_200 = 200
    NA = "N/A"
    TYPE = "type"
    KEY = "key"
    TITLE = "title"
    DATA = "data"
    VALUE = "value"
    STATE = "STATE"
    CHECK = "CHECK"
    doing = "doing"
    wait = "wait"
    STATE_FAILED = "STATE_FAILED"
    STATE_SUCCESS = "STATE_SUCCESS"
    STATE_RUNING = "STATE_RUNING"
    METHOD_INSERT_UPDATE = "INSERT_UPDATE"
    THE_DEV_USER = "the_dev_user"
    USERNAME = "username"
    PASSWORD = "password"
    METHOD_LOGIN = "login"
    METHOD_LOGIN_OUT = "login_out"
    METHOD_LOGIN_OK = "login_ok"
    METHOD_SUB = "sub"
    METHOD_UN_SUB = "un_sub"
    METHOD_DELETE = "DELETE"
    METHOD_EDIT = "EDIT"
    METHOD_SIMULATION = "SIMULATION"
    METHOD_ROLL_BACK = "ROLL_BACK"
    METHOD_CLONE = "CLONE"
    METHOD_FINISH = "FINISH"
    METHOD_RUN = "RUN"
    METHOD_INSERT = "INSERT"
    TOPIC_TASK_UPDATE_MSG = "TOPIC_TASK_UPDATE_MSG"
    TOPIC_F5_CHESS = "TOPIC_F5_CHESS"
    TOPIC_WEB_LOG = "TOPIC_WEB_LOG"
    TOPIC_MSG_QT = "TOPIC_MSG_QT"
    TOPIC_QT_CONFIG_UPDATE = "TOPIC_QT_CONFIG_UPDATE"
    TOPIC_AGENT_OUTPUT = "TOPIC_AGENT_OUTPUT"
    MSG_REGISTER = "register"
    MSG_REGISTER_OK = "register_ok"
    MSG_HEARTBEAT = "heartbeat"
    MSG_UNREGISTER = "unregister"
    MSG_EXEC = "exec"
    MSG_EXEC_STDOUT = "exec_stdout"
    MSG_EXEC_STDERR = "exec_stderr"
    MSG_EXEC_DONE = "exec_done"
    VIEW_STATE_CAN_EDIT = 1 << 0
    VIEW_SATTE_MAX = (1 << 8) - 1
    LAYOUT_ROW = "ROW"
    LAYOUT_COLUMN = "COLUMN"
    NEVER = "NEVER"
    SECOND1 = "SECOND1"
    SECOND30 = "SECOND30"
    MINUTE1 = "MINUTE1"
    MINUTE30 = "MINUTE30"
    EVERY_DAY_BEGIN = "EVERY_DAT_BEGIN"


class CT:
    MOD = (10**9) + 7
    MX = (10**5) + 1
    inf = float("inf")
    min = lambda a, b: a if a < b else b
    max = lambda a, b: a if a > b else b


C = THE_DEV_CONSTANT = Constant()
