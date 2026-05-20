import { Div } from "../div";
import { FlexColumn } from "../base/column";
import web_dom from "../../../web/web_dom"
import { not_null, Node } from "../../../web/cls"
import Constant from "../../../web/constant"
import { FormContainer } from "./container";
import { Button } from "./button";
import F from "../../../tool/fun";
import { FlexRow } from "../base/row";
export class FormColumn extends FlexRow {
    header: Div
    body: FlexRow
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
    init_style(): void {
        this.set_style({
            // textAlign: "center"
        })

        super.init_style()
    }
    init_node(): void {
        this.header = new Div()
        this.body = new FlexRow()
        this.footer = new FlexRow()
        this.foot_btns = {}
        this.add_children([
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
        if (o.data?.width) {
            r.container.set_width(o.data.width)
        }
        return r
    }
    render_chilld(d: Div, o: Node) {
        return d.set_flex_style_column()
    }
    render_children(children: Node[]) {
        this.child_map = {}
        this.body.clear()
        for (let o of children) {
            if (o.type === "form_row") {
                let rowContainer = new FlexRow()
                for (let child of o.children) {
                    let container = this.get_row(child)
                    container.set_style_row()
                    container.set_option(child).on_change(this.do_change.bind(this))
                    rowContainer.add_child(container)
                    this.child_map[child.key] = container
                }
                this.body.add_child(rowContainer)
            } else {
                let container = this.get_row(o)
                container.set_option(o).on_change(this.do_change.bind(this))
                this.body.add_child(container)
                this.child_map[o.key] = this.render_chilld(container, o)
            }
        }
        if (this.option.id) {
            web_dom.get_local(this.option.id, this.set_value.bind(this))
        }
    }
    render_main(v: Node): void {
        this.render_children(v.children)
        if (v.data.btns) {
            this.render_footer(v.data.btns)
        }
    }
    render_option(): void {
        this.render_main(this.option)
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
        this.event_hander[Constant.EVENT_SUBMIT]?.(type)
    }

    get_value(): any {
        let ret: { [key: string]: any } = {}
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