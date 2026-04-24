class Constant:
    APP_NAME = "TheDev"
    CODE_500 = 500
    CODE_200 = 200
    TYPE = "type"
    KEY = "key"
    DATA = "data"
    VALUE = "value"
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
    METHOD_DELETE = "DELETE"
    METHOD_EDIT = "EDIT"
    METHOD_FINISH = "FINISH"
    METHOD_INSERT = "INSERT"
    TOPIC_TASK_UPDATE_MSG = "TOPIC_TASK_UPDATE_MSG"
    TOPIC_WEB_LOG = "TOPIC_WEB_LOG"
    VIEW_STATE_CAN_EDIT = 1 << 0
    VIEW_SATTE_MAX = (1 << 8) - 1


class CT:
    MOD = (10**9) + 7
    MX = (10**5) + 1
    inf = float("inf")
    min = lambda a, b: a if a < b else b
    max = lambda a, b: a if a > b else b


C = THE_DEV_CONSTANT = Constant()
