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
    set_pos(x: number, y: number): this {
        this.set_attr("cx", x).set_attr("cy", y)
        return this
    }
}
export function circle() {
    return new Circle()
}