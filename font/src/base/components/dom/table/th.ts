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
    render_option(): void {
        this.set_html(this.option.title || this.option.value)
    }
}