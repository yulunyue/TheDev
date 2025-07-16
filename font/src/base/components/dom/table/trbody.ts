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
import { BodyTd } from "./td";
export class TrBody extends Div {
    field_map: object
    constructor() {
        super("tr", "")
    }
    row_idx: number
    set_row_idx(idx: number) {
        this.row_idx = idx
        return this
    }
    render_option(): void {
        this.field_map = {}

        this.clear().add_childs(this.option.childs.map(v => {
            this.field_map[v.key] = new BodyTd().set_row_idx(
                this.row_idx
            ).on_change(null).set_option(v)
            return this.field_map[v.key]
        }))
    }
    set_data(data: any) {
        for (var key in this.field_map) {
            this.field_map[key].set_value(data[key])
        }
        return this
    }

}