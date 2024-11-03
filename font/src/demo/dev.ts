import web_dom from "../base/web/web_dom";
import { DEV_COMPONENT, Node, Div } from "../base/components/export"
class Demo extends Div {
    init_node() {
        let childs = []
        for (var key in DEV_COMPONENT) {
            let child = DEV_COMPONENT[key]()
            // child.option = new Node().set_type(key)
            if (Array.isArray(child)) {
                childs = childs.concat(child)
            } else {
                childs.push(child)
            }
        }
        this.add_grid_childs(childs).abs_horizontal_layout()
    }
}
export default function () {
    return new Demo()
}