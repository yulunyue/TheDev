import { Div, div } from "../div";
import web from "../../../web/web_dom"
import { not_null, Node } from "../../../web/cls"

import Constant from "../../../web/constant"
import { Row } from "./row";
export class Form extends Div {
    header: Div
    body: Div
    footer: Div
    init_style(): void {
        this.set_style({
            textAlign: "center"
        })
    }
    init_node(): void {
        this.header = this.add_child(div())
        this.body = this.add_child(div())
        this.footer = this.add_child(div())

    }

    get_value() {
        // let ret = {}
        // for (var i = 0; i < this.rows.length; i++) {
        //     // console.log(this.childs[i])
        //     ret[this.rows[i].option.key] = this.rows[i].get_value()
        // }
        // return ret
    }
    get(key: string, default_value?: string) {
        return not_null(this.get_value()[key], default_value)
    }

}