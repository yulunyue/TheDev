import { GNode } from "./gnode"

import { Node, Point } from "../../web/cls"
import { Constant } from "../export"
export class Circle extends GNode {
    constructor() {
        super("circle")
    }
    init_style(): void {
        this.set_style({
            fill: Constant.COLOR_TANS,
            stroke: Constant.COLOR_BLACK
        })
    }
    set_r(radius: number) {
        this.set_attr("r", radius + "")
        return this
    }
    set_x(x: number) {
        return this.set_attr("cx", x)
    }
    set_y(y: number) {
        return this.set_attr("cy", y)
    }
    get_x() {
        return parseFloat(this.get_attr("cx"))
    }
    get_y() {
        return parseFloat(this.get_attr("cy"))
    }
    render_option(): void {
        let r = this.option.data.width / 2
        this.set_x(r).set_y(r).set_r(r - 3)
    }
}