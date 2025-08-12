import { GNode } from "./gnode"
import Constant from "../../web/constant";
export class Rect extends GNode {
    constructor() {
        super("rect")
    }
    init_style(): void {
        this.set_color(Constant.COLOR_BALCK)
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
export class Polygon extends GNode {
    constructor() {
        super("polygon")
    }
    set_points(points: any) {
        if (points == null || points == undefined) {
            return
        }
        if (Array.isArray(points)) {
            points = points.map(v => v[0] + "," + v[1]).join(' ')
        }
        return this.set_attr("points", points)
    }
    render_option(): void {
        this.set_points(this.option.value)
    }
}
export function polygon() {
    return new Polygon()
}
