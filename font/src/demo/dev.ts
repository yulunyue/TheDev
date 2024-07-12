import web_dom from "../base/web/web_dom";
import { Layout } from "../base/components/auto/layout";
import { DEV_COMPONENT } from "../base/components/export"
class Demo extends Layout {
    init() {
        let childs = []
        for (var key in DEV_COMPONENT) {
            childs.push(DEV_COMPONENT[key]())
        }
        this.add_grid_childs(childs)
        return this
    }
}
export default function () {
    return new Demo(Layout.VERTICAL).init().mount(web_dom.get_body()).on_mount()
}