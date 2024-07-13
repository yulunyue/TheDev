import { GNode } from "./gnode"
import { Point } from "../../tool/data"
export class Rect extends GNode {
    constructor() {
        super("rect")
    }
    set_wh(w: number, h: number) {
        return this.set_width(w).set_height(h)
    }
    set_width(x: number) {
        return this.set_attr("width", this.x(x))
    }
    set_height(y: number) {
        return this.set_attr("height", this.y(y))
    }

}
export function rect() {
    return new Rect()
}