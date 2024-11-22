import { GNode } from "./gnode"
import { Point } from "../../tool/data"
export class Line extends GNode {
    pts: Point[]
    src_y: number
    src_x: number
    dst_y: number
    dst_x: number
    constructor() {
        super("path")
        this.pts = []
    }

    init_style(): void {
        this.set_style({
            strokeWidth: "2",
            stroke: '#000',
            fill: "#000"
        })
    }
    set_d(pts: string | Point[]) {
        let ds = ""
        if (Array.isArray(pts)) {
            this.pts = pts
            for (var i = 0; i < pts.length; i++) {
                if (isNaN(pts[i].x) || isNaN(pts[i].y)) {
                    console.trace(pts[i])
                }
                if (i == 0) {
                    ds += `M ${pts[i].x} ${pts[i].y} `
                } else {
                    ds += `L ${pts[i].x} ${pts[i].y} `
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
    draw2() {
        if (isNaN(this.src_x) || isNaN(this.src_y) || isNaN(this.dst_y) || isNaN(this.dst_x)) {
            return this
        }
        this.set_d(`M ${this.src_x} ${this.src_y} L ${this.dst_x} ${this.dst_y}`)
        return this
    }
    set_src(y: number, x: number) {
        this.src_y = y
        this.src_x = x
        return this.draw2()
    }
    set_dst(y: number, x: number) {
        this.dst_y = y
        this.dst_x = x
        return this.draw2()
    }
    with_arrow_end() {
        return this.set_attr("marker-end", "url(#markerArrowEnd)")
    }
    with_arrow_start() {
        return this.set_attr("marker-start", "url(#markerArrow)")
    }
    with_arrow() {
        return this.with_arrow_end().with_arrow_start()
    }
}
export function line() {
    return new Line()
}