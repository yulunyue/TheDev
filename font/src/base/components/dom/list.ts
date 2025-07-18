import { Div } from "./div";
import { Node } from "../../web/cls";
import Ct from "../../web/constant"
import web_dom from "../../web/web_dom"
import { Label, label } from "./label";
export class ListUi extends Div {
    constructor() {
        super("div", "")
    }
    init_style(): void {
        this.set_style({
            overflowY: "auto"
        })
    }
    filter(s:any) { 
        this.set_option({filter_key:s})
    }
    get_row() {
        let lb =label().set_border()
        return lb.on_click(() => this.set_value(lb.option))
    }
    render_option(): void {
        console.log(this.option)
        if (this.option.childs) { 
            let childs = this.option.childs.filter((v: Node) => v.title.indexOf(this.option.filter_key) != -1)
            this.set_childs(childs, () => this.get_row())
        }
    }
}
export function listui() {
    return new ListUi()
}
export function listdev() {
    return listui()
}