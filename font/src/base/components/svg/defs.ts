import { GNode } from "./gnode";
import { line } from "./line";
import { Div, div } from "../dom/div"
export class Defs extends Div {
    constructor() {
        super("defs", "")
    }
    init_node(): void {
        this.add_child(div("marker").add_child(
            line()
        ))
    }
}
export function defs() {
    return new Defs()
}