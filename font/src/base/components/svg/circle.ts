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
            stroke: Constant.COLOR_BALCK
        })
    }
    set_r(radius: number) {
        if (!radius) {
            radius = 1
        }
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
        console.warn(this.option)
        this.set_x(this.option.x).set_y(this.option.y).set_r(this.option.value)
    }
}