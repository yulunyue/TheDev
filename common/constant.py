class Constant:
    APP_NAME = "TheDev"
    CODE_500 = 500
    CODE_200 = 200
    K_TYPE = "type"
    K_KEY = "key"
    K_DATA = "data"
    K_VALUE = "value"
    METHOD_INSERT_UPDATE = "INSERT_UPDATE"
    METHOD_LOGIN = "login"


class CT:
    MOD = (10**9) + 7
    MX = (10**5) + 1
    inf = float("inf")
    min = lambda a, b: a if a < b else b
    max = lambda a, b: a if a > b else b


C = THE_DEV_CONSTANT = Constant()
