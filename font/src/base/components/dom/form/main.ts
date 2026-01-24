import { Div } from "../div";
import web from "../../../web/web_dom"
import { not_null, Node } from "../../../web/cls"
import Constant from "../../../web/constant"
import { FormRow } from "./row";
export class Form extends Div {
    header: Div
    body: Div
    footer: Div
    init_style(): void {
        this.set_style({
            // textAlign: "center"
        })
    }
    init_node(): void {
        this.header = new Div()
        this.body = new Div()
        this.footer = new Div()
        this.add_childs([
            this.header,
            this.body,
            this.footer
        ])
    }
    get_row() {
        return new FormRow()
    }
    render_option(): void {
        console.log(this.option.childs)
        this.body.set_childs(this.option.childs, () => this.get_row())
    }
    get_value() {
        let ret = {}
        for (var i = 0; i < this.option.childs.length; i++) {
            let value = (this.body.childs[i] as FormRow).container.get_value()
            if (value == undefined) {
                value = null
            }
            ret[this.option.childs[i].key] = value
        }
        return ret
    }
    get(key: string, default_value?: string) {
        return not_null(this.get_value()[key], default_value)
    }

}