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
        this.body.set_childs(this.option.childs, () => this.get_row())

    }
    load_form_uri() {
        web.post(this.option.url + "/to_form_view", {}, (v: any) => {
            this.set_option(v)
        })
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
    set_uri(s: string): this {
        this.option.url = s
        this.load_form_uri()
        return this
    }

}