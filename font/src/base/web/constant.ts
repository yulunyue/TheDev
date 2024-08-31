import { Node } from "./cls"

function fack_data(depth: number, len: number) {
    let ret = new Node().set_title("root")
    if (depth == 0) {
        return ret
    }
    let childs = []
    for (var i = 0; i < len; i++) {
        childs.push(fack_data(depth - 1, len).set_title(
            `title_${depth}_${i}`
        ).set_value(
            `value_${depth}_${i}`
        ))
    }
    ret.set_childs(childs)
    return ret
}
class Constant {
    MOCK_KEY = "MOCK_KEY"
    MOCK_NODE_3_20 = fack_data(3, 20)
    MOCK_NODE_3_5 = fack_data(3, 5)
    get_mock_data(s: string) {
        if (s == this.MOCK_KEY) {
            return this.MOCK_NODE_3_20
        }
    }
}
export default new Constant()