import { Div, div } from "../div";
import web from "../../../web/web_dom"
import { not_null, Node } from "../../../web/cls"
import { Input, input } from "../input";
import { Button, button } from "../button";
import { Search, search } from "../search";
import { Select } from "../select";
import Constant from "../../../web/constant"
export class Row extends Div {
    title: Div
    body: Div
    input: Div
    static input_string: string = 'input'
    static text_area_string: string = 'text_area'
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
        if (this.option.title) {
            this.set_title(this.option.title)
        }
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
    on_change(call: any) {
        this.input.on_change(call)
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
        this.input.do_select(v)
        return this
    }
}