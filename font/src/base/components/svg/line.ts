import { GNode } from "./gnode"
import { Point } from "../../tool/data"
export class Line extends GNode {
    pts: Point[]
    constructor() {
        super("path")
        this.pts = []
    }
    init_style(): void {
        this.set_style({
            strokeWidth: "1",
            stroke: '#000',
            fill: "none"
        })
    }
    set_d(pts: string | Point[]) {
        let ds = ""
        if (Array.isArray(pts)) {
            this.pts = pts
            for (var i = 0; i < pts.length; i++) {
                if (i == 0) {
                    ds += `M ${this.x(pts[i].x)} ${this.y(pts[i].y)} `
                } else {
                    ds += `L ${this.x(pts[i].x)} ${this.y(pts[i].y)} `
                }
            }

        } else if (typeof (pts) == "string") {
            ds = pts
        }
        return this.set_attr("d", ds)
    }
    mount_d(pts: string | Point[]) {
        this.on_mount_call["set_d"] = [pts]
        return this
    }
    with_arrow() {
        return this.set_attr("marker-end", "url(#markerArrow)")
    }
}
export function line() {
    return new Line()
}