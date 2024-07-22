import { Div } from "./div";
import web from "../../web/web_dom"
export class Label extends Div {
    constructor() {
        super("p")
    }
    init_default_div_style() {

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
export function label() {
    return new Label()
}
export function label_dev() {
    return label().set_html(
        "label"
    ).click((v) => {
        console.log(v)
    })
}