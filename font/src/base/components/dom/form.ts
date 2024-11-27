import { Div, div } from "./div";
import web from "../../web/web_dom"
import { not_null, Node } from "../../web/cls"
import { Input, input } from "./input";
import { Button, button } from "./button";
import { Search, search } from "./search";
import { Select } from "./select";
import Constant from "../../web/constant"
export class Row extends Div {
    title: Div
    body: Div
    input: Div
    init_style(): void {
        this.set_style({ margin: 4, fontSize: 20 })
    }
    init_node(): void {
        this.title = this.add_child(div().set_style({
            // marginRight: 20,
            margin: Constant.DEFAULT_MARGIN
            // width: 100
        }))
        this.body = this.add_child(div())
        // this.set_style_flex(Constant.VERTICAL)
    }
    set_title(s: string) {
        this.title.set_html(s)
        return this
    }
    set_input(inp: any) {
        this.input = inp
        this.body.clear().add_child(inp)
        return this
    }
    render_option(): this {
        this.set_title(this.option.title)
        if (this.option.type == 'text') {
            this.set_input(new Div())
        } else if (this.option.type == 'search') {
            this.set_input(new Search())
        } else if (this.option.type == 'select') {
            this.set_input(new Select())
        }
        else if (this.option.type == 'input') {
            this.set_input(input())
        }
        this.input.set_option(this.option)
        return this
    }
    change(call: any) {
        this.input.change(call)
        return this
    }
    get_value() {
        return this.input.get_value()
    }
    set_value(v: any) {
        this.input.set_value(v)
        return this
    }
    select(v: any) {
        this.input.select(v)
        return this
    }
}
export class Form extends Div {
    header: Div
    body: Div
    footer: Div
    _dialog: Div
    _ok: any
    init_style(): void {
        this.set_style({
            textAlign: "center"
        })
    }
    init_node(): void {
        this.header = this.add_child(div())
        this.body = this.add_child(div())
        this.footer = this.add_child(div())
        this.footer.add_childs([
            button().set_html("确认").click(() => { this.do_ok() }),
            button().set_html("取消").click(() => { this.do_cancel() })
        ])
    }
    ok(call: any) {
        this._ok = call
        return this
    }
    do_ok() {
        this._ok?.(this.get_value())
        this._dialog?.hide()
    }
    do_cancel() {
        this._dialog?.hide()
    }
    set_rows(rows: Row[]) {
        this.body.clear().add_childs(rows)
        return this
    }
    get_value() {
        let ret = {}
        for (var i = 0; i < this.childs.length; i++) {
            ret[this.childs[i].option.key] = this.childs[i].get_value()
        }
        return ret
    }
    get(key: string, default_value?: string) {
        return not_null(this.get_value()[key], default_value)
    }

}
export function form() {
    return new Form()
}
export function row1() {
    return new Row().set_style_flex(Constant.VERTICAL)
}
export function row2() {
    return new Row()
}