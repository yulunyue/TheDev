import { Node } from "./cls"

function fack_data(depth: number, len: number) {
    let ret = new Node()
    if (depth == 0) {
        return ret
    }
    for (var i = 0; i < len; i++) {
        ret.childs.push(fack_data(depth - 1, len).set_title(
            `title_${depth}_${i}`
        ).set_value(
            `value_${depth}_${i}`
        ))
    }
    return ret
}
class Constant {
    MOCK_KEY = "MOCK_KEY"
    MOCK_DATA = { MOCK_KEY: fack_data(3, 20) }
    get_mock_data(s: string) {
        return this.MOCK_DATA[s]
    }
}
export default new Constant()