import { Div } from "./div";
import { Node } from "../../web/cls";
import Ct from "../../web/constant"
import web_dom from "../../web/web_dom"
import { Label } from "./base/label";
export class ListUi extends Div {
    constructor() {
        super("div", "")
    }
    init_style(): void {
        this.set_style({
            overflowY: "auto"
        })
    }
    filter(s: any) {
        this.set_option({ filter_key: s })
    }
    get_row() {
        let lb = new Label().set_border()
        return lb.on_click(() => this.set_value(lb.option))
    }
    render_option(): void {
        if (this.option.childs) {

            let childs = this.option.childs.filter(
                (v: Node) => v.title.indexOf(this.option.filter_key) != -1
            )
            this.option.data.size = childs.length
            this.set_childs(childs, () => this.get_row())

        }
    }
}