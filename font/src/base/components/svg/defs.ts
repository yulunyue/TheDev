import { GNode, gnode } from "./gnode";
import { line } from "./line";
export class Defs extends GNode {
    constructor() {
        super("defs")
    }
    init_node(): void {
        this.add_child(gnode("marker").add_child(
            line().set_d("M1,5 L11,10 L1,15 Z").set_color("#000")
        ).set_attr("id", "markerArrow").set_attr("viewBox", "0 0 20 20").set_attr(
            "markerWidth", "10"
        ).set_attr("markerHeight", "10").set_attr("refX", "11").set_attr(
            "refY", "10"
        ).set_attr("orient", "auto"))
    }
}
export function defs() {
    return new Defs()
}