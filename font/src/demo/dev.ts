import web_dom from "../base/web/web_dom";
import { Div } from "../base/components/export";
import { mera_util, MeraUtil } from "../base/components/svg/comb/mermaid_util";
class Demo extends Div {
    init_node() {
        this.add_child(mera_util())
    }
}
export default function () {
    return new Demo()
}