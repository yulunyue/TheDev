import { Div } from "../div";
import web from "../../../web/web_dom"
import { Constant, Node } from "../../export";
export class Label extends Div {
    text: string = null
    change_color: string = null
    constructor() {
        super("p")
    }
    init_style(): void {
        this.set_style({
            fontFamily: Constant.DEFAULT_FONT_FAMILY,
            fontSize: Constant.DEFAULT_FONT_SIZE,
            textWrap: "wrap"
        })
    }
    set_value(value: any): this {
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
export class Span extends Div {
    constructor() {
        super("span")
    }
    set_value(value: any): this {
        return this.set_html(value)
    }
}

export class Pre extends Div {
    constructor() {
        super("pre")
    }
    init_node(): void {

    }
    set_value(value: any): this {
        if (value instanceof Object) {
            value = JSON.stringify(value, null, 2)
        }
        return this.set_html(value)
    }
    init_style(): void {
        this.set_style({
            whiteSpace: "pre-wrap",
            overflowWrap: "break-word",
            overflowY: "auto"
        })
    }
    render_option() {
        this.set_value(this.option.value)
    }
}

