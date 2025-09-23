class Constant:
    APP_NAME = "TheDev"
    MOD = (10**9) + 7
    inf = float("inf")
    WEB_VIEW_TYPE_ENUM = "enum"
    WEB_VIEW_TYPE_SEARCH = "search"
    WEB_VIEW_TYPE_TABLE = "table"
    KEY_BODY = "body"
    CODE_500 = 500
    CODE_200 = 200
    STATE_WAIT = "WAIT"
    STATE_DOING = "DOING"
    STATE_FINISH = "FINISH"
    STATE_ERROR = "ERROR"
    FlowChartTD = "flowchart TD"


class CT:
    MOD = (10**9) + 7
    MX = (10**5) + 1
    inf = float("inf")
    min = lambda a, b: a if a < b else b
    max = lambda a, b: a if a > b else b


THE_DEV_CONSTANT = Constant()
