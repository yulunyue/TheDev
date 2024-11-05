import { Node } from "./cls"

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

    INPUT_NUMBER_WIDTH = 40

    KEY_RIGHT = 'ArrowRight'
    KEY_LEFT = 'ArrowLeft'
    MOCK_NODE_3_20 = fack_data(0, 3, 20)
    MOCK_NODE_3_5 = fack_data(0, 3, 5)
    MOCK_NODE_3_3 = fack_data(0, 3, 3)
    get_mock_data(s: string) {
        if (s == this.MOCK_KEY) {
            return this.MOCK_NODE_3_20
        }
    }
}
export default new Constant()