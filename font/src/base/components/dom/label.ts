import { Div } from "./div";
import web from "../../web/web_dom"
import { Constant } from "../export";
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
        })
    }
    set_text(s: any) {
        if (typeof s == 'string') {
            this.set_titles([s])
        } else {
            this.set_titles(s)
        }
    }
    set_titles(s: string[]) {
        for (var i = 0; i < s.length; i++) {
            this.get_child(i, lb).set_html(s[i])
        }
    }
    render_option() {
        this.set_text(this.option.title)
    }
}
export function label() {
    return new Label()
}
export function pre() {
    return new Pre()
}