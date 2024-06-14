import { Div } from "./div";

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
    return new Button().set_html("button")
}