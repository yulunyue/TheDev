import { GNode } from "./gnode"
import { Point } from "../../tool/data"
import { Node } from "../../web/cls"
export class Circle extends GNode {
    constructor() {
        super("circle")
    }
    set_r(radius: number) {
        if (!radius) {
            radius = 1
        }
        this.set_attr("r", radius + "")
        return this
    }
    set_x(x: number) {
        return this.set_attr("cx", this.x(x))
    }
    set_y(y: number) {
        return this.set_attr("cy", this.y(y))
    }
    get_x() {
        return parseFloat(this.get_attr("cx"))
    }
    get_y() {
        return parseFloat(this.get_attr("cy"))
    }
    set_option(option: Node): this {
        if (!option.data) {
            return this
        }
        return this.set_x(
            option.data.x
        ).set_y(
            option.data.y
        ).set_r(option.data.r)
    }
}
export function circle() {
    return new Circle()
}