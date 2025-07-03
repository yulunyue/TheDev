import { Div } from "./div";
import web from "../../web/web_dom"
import { Constant, Node } from "../export";
export class Label extends Div {
    text: string = null
    change_color: string = null
    constructor() {
        super("span")
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
    set_change_color(color: string) {
        this.change_color = color
        return this
    }
    click(call_back: any) {
        web.bind_mouseenter(this.el, () => {
            this.set_style({
                backgroundColor: "green"
            })
        })
        web.bind_mouseleave(this.el, () => {
            this.set_style({
                backgroundColor: "white"
            })
        })
        return super.click(call_back)
    }

}
function lb() {
    return new Label().set_change_color(Constant.COLOR_BLUE)
}
export function label() {
    return new Label()
}
export class Pre extends Div {

    constructor() {
        super("pre")
    }
    init_node(): void {

    }
    init_style(): void {
        this.set_style({
            //padding: Constant.DEFAULT_PADDING,

            //textWrap: "wrap"
            overflowY: "auto"
        })
    }
    set_text(s: any) {
        if (Array.isArray(s)) {
            this.set_titles(s)
        } else {
            this.set_titles([s])
        }
    }
    set_titles(s: Node[]) {
        for (var i = 0; i < s.length; i++) {
            let title = s[i].value
            if (s[i].title) {
                title = s[i].title + ' : ' + s[i].value
            }
            this.get_child(i, lb).set_html(title).set_color(s[i].color)
        }
    }
    render_option() {
        this.set_text(this.option.data)
    }
}

export function pre() {
    return new Pre()
}