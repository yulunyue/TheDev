import { Div } from "../div";
import web_dom from "../../../web/web_dom"
import Constant from "../../../web/constant";

export class Checkbox extends Div {
    el: HTMLInputElement
    constructor() {
        super("input")
    }
    init_node() {
        this.el.setAttribute("type", "checkbox")
    }
    init_style(): void {
        this.set_style({
            margin: Constant.DEFAULT_MARGIN,
            width: "20px",
            height: "20px"
        })
    }
    render_option() {
        this.set_value(this.option.value)
    }
    set_value(value: any) {
        this.el.checked = Boolean(value)
        return this
    }
    get_value() {
        return this.el.checked
    }
    on_change(call: any): this {
        this.el.onchange = () => {
            call(this.option.key, null, this.el.checked)
        }
        return this
    }
}