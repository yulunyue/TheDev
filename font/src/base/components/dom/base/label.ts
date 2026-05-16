import { Div } from "../div";
import web from "../../../web/web_dom"
import { Constant, Node } from "../../export";
export class Label extends Div {
    text: string | null = null
    change_color: string | null = null
    constructor() {
        super("p")
    }
    init_style(): void {
        this.set_style({
            fontFamily: Constant.DEFAULT_FONT_FAMILY,
            fontSize: Constant.DEFAULT_FONT_SIZE,
            textWrap: "wrap",
            textOverflow: "ellipsis"

        })
    }
    set_value(value: any): this {
        if (typeof value == "object") {
            value = JSON.stringify(value)
        }
        this.set_html(value)
        return this
    }
    render_option(): void {
        this.set_html(this.option.title)
    }
    set_change_color(color: string) {
        this.change_color = color
        return this
    }
    on_click(call_back: any) {
        web.bind_mouseenter(this.el, () => {
            this.set_style({
                backgroundColor: "#888"
            })
        })
        web.bind_mouseleave(this.el, () => {
            this.set_style({
                backgroundColor: "white"
            })
        })
        return super.on_click(call_back)
    }

}



