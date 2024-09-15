import { Div } from "./div";
import { Style, Node, Fn1 } from "../../web/cls"
export class Button extends Div {
    constructor() {
        super("button")
    }
    init_node() {

    }
    init_style(): void {
        this.set_style({ outline: "none" })
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