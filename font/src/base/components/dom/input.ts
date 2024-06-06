import { Div } from "./div";

export class Input extends Div {
    init_node() {
        this.el = Div.create_element("input")
    }
    init_style(): void {
        this.set_style({ outline: "none" })
    }
}
export function input() {
    return new Input()
}