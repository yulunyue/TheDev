import { Div } from "../div";
import { FlexRow } from "../base/column";
import web_dom from "../../../web/web_dom"
import { not_null, Node } from "../../../web/cls"
import Constant from "../../../web/constant"
import { FormContainer } from "./container";
import { Button } from "./button";
import F from "../../../tool/fun";
export class FormRow extends Div {
    header: Div
    body: Div
    footer: FlexRow
    _submit_call_back: any
    input_width: number
    child_map: any
    foot_btns: any
    set_input_width(width: number) {
        this.input_width = width
        return this
    }
    on_submit(call: any) {
        this.event_hander[Constant.EVENT_SUBMIT] = call
        return this
    }
    on_mock_get_value(call: any) {
        this.event_hander[Constant.EVENT_MOCK_GET_VALUE] = call
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
        this.footer = new FlexRow()
        this.foot_btns = {}
        this.add_childs([
            this.header,
            this.body,
            this.footer
        ])
    }
    do_change(key: string, src?: any, dst?: any) {
        if (this.option.id) {
            web_dom.set_local(this.option.id, this.get_value())
        }
        return super.do_change(key, src, dst)
    }
    get_row(o: Node) {
        let r = new FormContainer()
        if (this.input_width) {
            r.container.set_width(this.input_width)
        }
        return r
    }
    render_childs(childs: Node[]) {
        this.body.set_childs(childs, this.get_row.bind(this))
        this.child_map = {}
        for (var i = 0; i < childs.length; i++) {
            let o = childs[i]
            this.body.childs[i].set_option(o).on_change(this.do_change.bind(this))
            this.child_map[o.key] = this.body.childs[i]
        }
        if (this.option.id) {
            web_dom.get_local(this.option.id, this.set_value.bind(this))
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

    }
    render_footer(btns: any) {
        for (var key in btns) {
            if (this.foot_btns[key]) {
                continue
            }
            let btn = new Button().set_html(btns[key])
            btn.on_click(F.register_call((tp: string) => this.submit_hander(tp), key))
            this.foot_btns[key] = btn
            this.footer.add_child(btn)
        }
    }
    set_btns(btns: any) {
        this.render_footer(btns)
        for (var key in this.foot_btns) {
            if (btns[key]) {
                this.foot_btns[key].show()
            } else {
                this.foot_btns[key].hide()
            }
        }
        return this
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
    get_value(): any {
        let ret = {}
        for (var key in this.child_map) {
            let value = this.child_map[key].get_value()
            ret[key] = value
        }
        if (this.event_hander[Constant.EVENT_MOCK_GET_VALUE]) {
            return this.event_hander[Constant.EVENT_MOCK_GET_VALUE](ret)
        }
        return ret
    }
    get(key: string, default_value?: string) {
        return not_null(this.get_value()[key], default_value)
    }

    set_value(value: any): this {
        for (var key in this.child_map) {
            // console.log(key, value, value[key], this.child_map[key])
            this.child_map[key].set_value(value[key])
        }
        return this
    }

}