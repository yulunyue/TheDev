import web_dom from "../base/web/web_dom";
import { Layout } from "../base/components/auto/layout";
import { DEV_COMPONENT } from "../base/components/export"
class Demo extends Layout {
    init() {
        for (var key in DEV_COMPONENT) {
            this.add_child(DEV_COMPONENT[key]())
        }
        return this
    }
}
export default function () {
    return new Demo(Layout.VERTICAL).init().mount(web_dom.get_body()).on_mount()
}