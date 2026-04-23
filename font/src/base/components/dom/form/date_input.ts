import { Div } from "../div";
import web_dom from "../../../web/web_dom"
import Constant from "../../../web/constant";

export class DateInput extends Div {
    el: HTMLInputElement
    constructor() {
        super("input")
    }
    init_node() {
        this.el.setAttribute("type", "date")
    }
    init_style(): void {
        this.set_style({
            outline: "none",
            margin: Constant.DEFAULT_MARGIN,
            padding: Constant.DEFAULT_PADDING,
            width: `calc(100% - ${(Constant.DEFAULT_MARGIN + Constant.DEFAULT_PADDING) * 2}px)`
        })
    }
    render_option() {
        this.set_value(this.option.value)
    }
    set_value(value: any) {
        if (value) {
            let dateStr = value
            if (typeof value === "string" && value.includes("-")) {
                dateStr = value
            } else if (Array.isArray(value) && value.length === 3) {
                dateStr = `${value[0]}-${String(value[1]).padStart(2, '0')}-${String(value[2]).padStart(2, '0')}`
            }
            this.el.value = dateStr
        }
        return this
    }
    get_value() {
        return this.el.value
    }
    on_change(call: any): this {
        this.el.onchange = () => {
            call(this.option.key, null, this.el.value)
        }
        return this
    }
}