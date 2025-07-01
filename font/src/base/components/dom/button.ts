import { Div } from "./div";
import { Style, Node, Fn1 } from "../../web/cls"
import Constant from "../../web/constant";
export class Button extends Div {
    constructor() {
        super("button")
    }
    init_node() {

    }
    init_style(): void {
        this.set_style({
            outline: "none",
            margin: Constant.DEFAULT_MARGIN,
            padding: Constant.DEFAULT_PADDING
        })
    }
}
export class Buttons extends Div {
    render_option(): void {
        this.clear().add_childs(this.option.childs.map(v => {
            return new Button().set_html(v.title)
        }))
    }
}
export class Title extends Div {
    title: Div
    btns: Button[]
    init_node(): void {
        this.title = this.add_child(new Div()).set_size(1)
    }
    set_btns(btns: Button[]) {
        this.add_childs(btns)
        return this
    }
}
export function button() {
    return new Button()
}
