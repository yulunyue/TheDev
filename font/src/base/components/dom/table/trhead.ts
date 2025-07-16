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
import { Th } from "./th";
import { TrBody } from "./trbody";
export class TrHead extends Div {
    constructor() {
        super("tr", "")
    }
    init_style(): void {
        this.set_style({
            border: "1px solid #000",
            position: "sticky",
            top: 0,
            zIndex: "10",
            backgroundColor: "#fff",
        })
    }
    render_option() {
        this.clear().add_childs(this.option.childs.map(v => {
            return new Th().set_option(v)
        }))
        return this
    }

    new_dom_row(idx: number) {
        return new TrBody().set_row_idx(idx).on_change(
            //this._on_change
            null
        ).set_option(this.option)
    }
    add_one_row() {

    }

}