import { Node } from "./cls"
import web_dom from "./web_dom"
import util from "../tool/util"


class Constant {
    DEFAULT_MARGIN = 4
    DEFAULT_PADDING = 3
    DEFAULT_LINE_HEIGHT = 40

    MOCK_KEY = "MOCK_KEY"

    HORIZONTAL = 0
    VERTICAL = 1

    COLOR_WHITE = '#fff'
    COLOR_WHITE1 = '#eee'
    COLOR_WHITE2 = '#ccc'
    COLOR_YELLOW = '#ff0'
    COLOR_BALCK = '#000'
    COLOR_BALCK2 = '#222'
    COLOR_BLUE = '#00f'
    COLOR_GRAY = '#888'
    COLOR_TANS = 'transparent'
    DEFAULT_FONT_FAMILY = "'Times New Roman', serif"
    DEFAULT_FONT_SIZE = "12px"
    DIALOG_COLOR = '#8888'


    INPUT_NUMBER_WIDTH = 20
    INPUT_STR_WIDTH = 100
    INPUT_HEIGHT = 40
    INPUT_STRING_MIN_WIDTH = 50
    TEXT_AREA_WIDTH = 600
    TEXT_AREA_HEIGHT_1 = 100
    TEXT_AREA_HEIGHT_2 = 200
    TEXT_AREA_HEIGHT_3 = 400
    WIDTH_TEXT = 200

    KEY_RIGHT = 'ArrowRight'
    KEY_LEFT = 'ArrowLeft'

    NUMBER = "number"


    Z_INDEX_1 = "1"

    EVENT_CHANGE = "event_change"
    EVENT_SUBMIT = "event_submit"
    EVENT_MOVE = "event_move"
    EVENT_CLICK = "event_click"
    DOM_TYPE_SELECT = "select"
    DOM_TYPE_INPUT = "input"
    DOM_TYPE_TITLE = "title"
    DOM_TYPE_STRING = "str"
    SVG_TYPE_CIRCLE = "circle"
    DOM_TYPE_MERA_GRAPH = "graph"
    DOM_TYPE_D3_CHART = "d3chart"
    DOM_TYPE_PRE = "pre"
    DOM_TYPE_ENUM = "enum"
    DOM_TYPE_SEARCH = "search"
    DOM_TYPE_TABLE = "table"
    DOM_TYPE_GRID = "grid"
    DOM_TYPE_NUMBER = "number"
    DOM_TYPE_FILE = "DomFile"
    DOM_TYPE_FORM_ROW = "form_row"
    DOM_TYPE_FORM_COLUMN = "form_column"
    DOM_TYPE_ROW = "row"
    DOM_TYPE_COLUMN = "column"
    DOM_TYPE_BUTTON = "button"
    the_dev_user = "the_dev_user"
    username = "username"
    METHOD_LOGIN = "login"
    METHOD_SEND_TO = "send_to"

}
export default new Constant()