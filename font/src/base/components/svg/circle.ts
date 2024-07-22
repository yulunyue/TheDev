import { GNode } from "./gnode"
import { Point } from "../../tool/data"
export class Circle extends GNode {
    constructor() {
        super("circle")
    }
    set_r(radius: number) {
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
}
export function circle() {
    return new Circle()
}