import { Div } from "./div";
import web from "../../web/web_dom"
import { Constant } from "../export";
export class Label extends Div {
    constructor() {
        super("p")
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
export class Pre extends Div {
    constructor() {
        super("pre")
    }
    init_style(): void {
        this.set_style({
            padding:Constant.DEFAULT_PADDING,
            textWrap:"wrap"
        })
    }
}
export function label() {
    return new Label()
}
export function pre() {
    return new Pre()
}