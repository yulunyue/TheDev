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
export class Title extends Div {
    title: Div
    btns: Button[]
    init_node(): void {
        this.title = this.add_child(new Div())
    }
    set_btns(btns: Button[]) {
        this.add_childs(btns)
        return this
    }
}
export function button() {
    return new Button()
}
export function button_dev() {
    return [
        button().set_html("button"),
        button().set_option(new Node().set_type("edit"))
    ]
}