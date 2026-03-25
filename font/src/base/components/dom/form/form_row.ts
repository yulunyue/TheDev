import { Div } from "../div";
import web_dom from "../../../web/web_dom"
import { not_null, Node } from "../../../web/cls"
import Constant from "../../../web/constant"
import { FormContainer } from "./container";
import { Button } from "./button";
import F from "../../../tool/fun";
import { url } from "inspector";
export class FormRow extends Div {
    header: Div
    body: Div
    footer: Div
    _submit_call_back: any
    on_submit(call: any) {
        this.event_hander[Constant.EVENT_SUBMIT] = call
        return this
    }
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
    get_row(o: Node) {
        let r = new FormContainer().set_option(o).on_change(this.do_change)
        this.child_map[o.key] = r
        return r
    }
    render_childs(childs: any) {
        this.body.set_childs(childs, (o: Node) => this.get_row(o))
        if (this.option.id) {
            web_dom.get_local(this.option.id, (v: any) => this.set_value(v))
        }
    }
    render_option(): void {
        if (this.option.url) {
            web_dom.post(this.option.url + this.get_form_view_url(), {}, (v: any) => {
                this.render_childs(v.childs)
            })
        } else {
            this.render_childs(this.option.childs)
        }
        this.render_footer()
    }
    render_footer() {
        let btns = this.option.data.btns || { insert: "提交" }
        this.footer.clear()
        for (var key in btns) {
            let btn = new Button().set_html(btns[key])
            btn.on_click(F.register_call((tp: string) => this.submit_hander(tp), key))
            this.footer.add_child(btn)
        }
    }
    submit_hander(type: string) {
        if (this.option.url) {
            web_dom.post(this.option.url + "/web_submit", {
                type: type,
                value: this.get_value()
            }, (data: Node) => {
                this.event_hander[Constant.EVENT_SUBMIT]?.(type, data.value)
            })
        } else {
            this.event_hander[Constant.EVENT_SUBMIT]?.(type, this.get_value())
        }
    }
    get_form_view_url() {
        return "/to_form_row_view"
    }
    load_form_uri() {

    }
    get_value() {
        let ret = {}
        for (var i = 0; i < this.option.childs.length; i++) {
            let value = (this.body.childs[i] as FormContainer).container.get_value()
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

    set_value(value: any): this {
        console.log(value)
        for (var key in this.child_map) {
            // console.log(key, value, value[key], this.child_map[key])
            this.child_map[key].set_value(value[key])
        }
        return this
    }

}