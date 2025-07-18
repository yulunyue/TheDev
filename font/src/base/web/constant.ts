import { Node } from "./cls"
import web_dom from "./web_dom"
import util from "../tool/util"
import MOCK_DATA from "../../model/mock"
function fack_data(depth: number, max_dp: number, len: number) {
    let ret = new Node().set_title("root")
    if (depth == max_dp) {
        return ret
    }
    let childs = []
    for (var i = 0; i < len; i++) {
        childs.push(fack_data(depth + 1, max_dp, len).set_title(
            `title_${depth}_${i}`
        ).set_value(
            `value_${depth}_${i}`
        ))
    }
    ret.set_childs(childs)
    return ret
}
class Constant {
    DEFAULT_MARGIN = 4
    DEFAULT_PADDING = 3
    DEFAULT_LINE_HEIGHT = 40

    MOCK_KEY = "MOCK_KEY"

    HORIZONTAL = 0
    VERTICAL = 1

    COLOR_WHITE = '#fff'
    COLOR_YELLOW = '#ff0'
    COLOR_BALCK = '#000'
    COLOR_BLUE = '#00f'
    COLOR_GRAY = '#888'
    COLOR_TANS = 'transparent'
    DEFAULT_FONT_FAMILY = "'Times New Roman', serif"
    DEFAULT_FONT_SIZE = "12px"
    DIALOG_COLOR = '#8888'


    INPUT_NUMBER_WIDTH = 20
    INPUT_STRING_MIN_WIDTH = 50
    TEXT_AREA_WIDTH = 600
    TEXT_AREA_HEIGHT_1 = 100
    TEXT_AREA_HEIGHT_2 = 200
    TEXT_AREA_HEIGHT_3 = 400


    KEY_RIGHT = 'ArrowRight'
    KEY_LEFT = 'ArrowLeft'

    NUMBER = "number"

    MOCK_NODE_3_20 = fack_data(0, 3, 20)
    MOCK_NODE_3_5 = fack_data(0, 3, 5)
    MOCK_NODE_3_3 = fack_data(0, 3, 3)

    Z_INDEX_1 = "1"

    DATA_SOURCE_DYN = "data_source_dyn"

    EVENT_CHANGE = "event_change"

    DOM_TYPE_INPUT = "input"
    DOM_TYPE_MERA_GRAPH = "graph"
    DOM_TYPE_PRE = "pre"
    get_mock_data(s: string, param: any) {
        if (web_dom.web_host.endsWith('github.io')) {
            return this.get_ts_data(s, param)
        }
        return null
    }
    get_ts_data(s: string, param: any) {
        let param_hash = util.hash_any(param)
        if (MOCK_DATA[s] && MOCK_DATA[s][param_hash])
            return MOCK_DATA[s][param_hash]
        return null
    }
}
export default new Constant()