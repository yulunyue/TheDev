import { Div } from "./div";
export class Label extends Div {
    constructor() {
        super("p")
    }
}
export function label() {
    return new Label().set_html("label")
}