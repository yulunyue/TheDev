import { Div } from "../div";
import Ct from "../../../web/constant"
import web from "../../../web/web_dom"
import { Node, to_node } from "../../../web/cls";
import { Input } from "../form/input";
import { Label } from "../base/label"
import { Pagination } from "../../combo/pagination";
import Util from "../../../tool/util"
import { Constant } from "../../export";
export class Th extends Div {
    constructor() {
        super("th")
    }
    init_style(): void {
        this.set_style({
            position: "sticky",
            top: 0
        })
    }
    set_value(value: any): this {
        if (typeof value == "object") {
            value = JSON.stringify(value)
        }
        this.set_html(value)
        return this
    }
    render_option(): void {
        this.set_value(this.option.title)
    }
}