import { Div } from "../div";
import web_dom from "../../../web/web_dom"
import Constant from "../../../web/constant";
export class Input extends Div {
    el: HTMLInputElement
    constructor() {
        super("input")
    }
    init_node() {

    }
    on_input(call: any) {
        web_dom.bind_input(this.el, call)
        return this
    }
    set_placeholder(title: string) {
        return this.set_attr("placeholder", title)
    }
    init_style(): void {
        this.set_style({
            outline: "none",
            margin: Constant.DEFAULT_MARGIN,
            padding: Constant.DEFAULT_PADDING,
            width: `calc(100% - ${(Constant.DEFAULT_MARGIN + Constant.DEFAULT_PADDING) * 2}px)`,
            borderTop: "none",
            borderLeft: "none",
            borderRight: "none",

        })
    }
    render_option() {
        if (this.option.type == Constant.NUMBER) {
            this.set_width(Constant.INPUT_NUMBER_WIDTH)
        }
        this.set_value(this.option.value)
    }
    set_value(value: any) {
        // console.log("set_value", value)
        this.el.value = value
        return this
    }
    get_value() {
        return this.el.value
    }
    get_int() {
        let ret = parseInt(this.get_value())
        if (isNaN(ret)) {
            ret = 0
        }
        return ret
    }
    on_change(call: any): this {
        // this.el.onchange = call
        this.el.oninput = call
        return this
    }

}


