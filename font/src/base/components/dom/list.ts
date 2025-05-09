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
    set_flex_style(direction: number, use_border?: boolean): this {
        return this
    }
    set_path(path: any, data?: any) {
        web_dom.post(path, data, (v: Node) => {
            this.set_option(v)
        })
        return this
    }
    get_row(v:Node) { 
        return label().set_html(v.title).set_option(v).set_border()
    }
    set_option(option: Node) {
        this.clear().add_childs(option.childs.map(v => this.get_row(v)))
        return this

    }
    select(callback: any) {
        this.childs.map(v => {
            v.click(() => {
                callback(v.option)
            })
        })
        return this
    }
}
export function listui() {
    return new ListUi()
}
export function listdev() {
    return listui().set_path(Ct.MOCK_KEY).select((v) => {
        console.log(v)
    })
}