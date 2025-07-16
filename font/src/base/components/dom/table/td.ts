import { Div } from "../div";
import Ct from "../../../web/constant"
import web from "../../../web/web_dom"
import { Node, to_node } from "../../../web/cls";
import { Input } from "../input";
import { Button, Buttons } from "../button";
import { Label } from "../label"
import { Pagination } from "../pagination";
import Util from "../../../tool/util"
import { Constant } from "../../export";
export class HeadTd extends Div {
    ins: Div
    constructor() {
        super("td", "")
    }
    render_option(): void {
        let ins = new Label().set_html(this.option.value)
        this.ins = this.clear().add_child(ins)
    }
}
export class BodyTd extends HeadTd {
    row_idx: number
    set_row_idx(idx: number) {
        this.row_idx = idx
        return this
    }
    init_style(): void {

    }
    render_option(): void {
        let ins = null
        if (this.option.type == "input") {
            ins = new Input().set_value(this.option.value)
        }
        else if (this.option.type == 'btns') {
            ins = new Buttons().set_option(to_node({
                childs: this.option.value.map((v: any) => {
                    return { title: v }
                })
            }))
        }
        else {
            ins = new Label().set_html(this.option.title || this.option.value)
        }
        this.ins = this.clear().add_child(ins).on_change(() => {
            //this._on_change({ idx: this.row_idx, key: this.option.key, value: this.ins.get_value() })
        })
    }
    set_value(value: any) {
        this.ins.set_value(value)
        return this
    }

}