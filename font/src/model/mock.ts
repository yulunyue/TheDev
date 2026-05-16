import { Node } from "../base/web/cls"
class Mock {

    fake_data(depth: number, max_dp: number, len: number) {
        let ret = new Node().set_title("root")
        if (depth == max_dp) {
            return ret
        }
        let children = []
        for (var i = 0; i < len; i++) {
            children.push(this.fake_data(depth + 1, max_dp, len).set_title(
                `title_${depth}_${i}`
            ).set_value(
                `value_${depth}_${i}`
            ))
        }
        ret.set_children(children)
        return ret
    }
    fake_data_matrix(x: number, y: number) {
        let ret = new Node()
        for (var i = 0; i < y; i++) {
            for (var j = 0; j < x; j++) {
                ret.add_child(new Node().set_option({
                    y: i,
                    x: j
                }))
            }
        }
        return ret
    }

}
export default new Mock()