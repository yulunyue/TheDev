import { Div } from "../div";
import Ct from "../../../web/constant"
import web from "../../../web/web_dom"
import { Node, to_node } from "../../../web/cls";
import { Input } from "../form/input";
import { Label } from "../base/label"
import { Pagination } from "../../combo/pagination";
import Util from "../../../tool/util"
import { Constant } from "../../export";
import { TrHead } from "./trhead";
export class TBody extends Div {
    constructor() {
        super("tbody")
    }
    init_style(): void {
        this.set_style({
            maxHeight: 400,
            overflowY: "auto"
        })
    }
    render_option() {
        this.clear().add_children(this.option.children.map(v => {
            let tr = new TrHead().set_option(v)
            return tr.on_change(null)
        }))
        return this
    }
}