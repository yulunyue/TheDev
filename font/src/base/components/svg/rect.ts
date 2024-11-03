import { GNode } from "./gnode"
import Constant from "../../web/constant";
import { Point } from "../../tool/data"
export class Rect extends GNode {
    constructor() {
        super("rect")
    }
    init_style(): void {
        this.set_color(Constant.COLOR_WHITE)
    }
    set_wh(w: number, h: number) {
        return this.set_width(w).set_height(h)
    }
    set_width(x: number) {
        return this.set_attr("width", x)
    }
    set_height(y: number) {
        return this.set_attr("height", y)
    }

}
export function rect() {
    return new Rect()
}