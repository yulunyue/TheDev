import { Div, Container } from "../div";
import web from "../../../web/web_dom"
import { not_null, Node } from "../../../web/cls"
import { Search } from "./search";
import { Select } from "./select";
import Constant from "../../../web/constant"
export class FormContainer extends Div {
    title: Div
    body: Div
    container: Container
    init_style(): void {
        this.set_style({ margin: Constant.DEFAULT_MARGIN })
        this.title.set_style({
            margin: Constant.DEFAULT_MARGIN,
            width: 80
        })
    }
    init_node(): void {
        this.title = new Div()
        this.container = new Container()
        this.add_children([
            this.title,
            this.container
        ])
    }

    set_title(s: string) {
        this.title.set_html(s)
        return this
    }
    set_option(option: Node): this {
        option.type = option.type || Constant.DOM_TYPE_INPUT
        option.title = option.title || option.key
        return super.set_option(option)
    }
    render_option(): this {
        this.container.set_option(this.option)
        return this
    }
    set_value(value: any): this {
        this.container.main.set_value(value)
        return this
    }
    disable(state: boolean) {
        this.container.main.disable(state)
        return this
    }
    on_change(call: any) {
        this.container.main.on_change(call)
        return this
    }
    get_value() {
        return this.container.main.get_value()
    }
}