import { Container, Div } from "../div";
import Ct from "../../../web/constant"
import web from "../../../web/web_dom"
import { Node, to_node } from "../../../web/cls";
import { Input } from "../form/input";
import { Button } from "../form/button";
import { Label } from "../base/label"
import { Pagination } from "../../combo/pagination";
import Util from "../../../tool/util"
import { Constant } from "../../export";
export class HeadTd extends Div {
    ins: Div
    constructor() {
        super("td")
    }
    render_option(): void {
        let ins = new Label().set_html(this.option.value)
        this.ins = this.clear().add_child(ins)
    }
}
export class BodyTd extends HeadTd {
    row_idx: number
    ins: Container
    init_node(): void {
        this.ins = new Container()
        this.add_child(this.ins)
    }
    set_row_idx(idx: number) {
        this.row_idx = idx
        return this
    }
    init_style(): void {
        this.ins.set_style({
            maxHeight: Constant.TABLE_ROW_MIN_HEIGHT,
            overflow: "auto"
        })
        this.set_style({
            textOverflow: "ellipsis"
        })
    }
    set_option(o: Node) {
        this.ins.set_option(o)
        return this
    }
    set_value(value: any) {
        this.ins.set_value(value)
        return this
    }

}