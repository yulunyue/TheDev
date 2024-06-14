import { Div } from "./div";

export class Input extends Div {
    constructor() {
        super("input")
    }
    init_node() {

    }
    init_style(): void {
        this.set_style({ outline: "none" })
    }
}
export function input() {
    return new Input()
}