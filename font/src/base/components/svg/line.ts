import { GNode } from "./gnode"
import { Defs, ARROW_KEY, ARROW_START, ARROW_END } from "./defs"
export class Line extends GNode {
    pts: any[]
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
            fill: "#fff"
        })
    }
    set_d(pts: string | any[]) {
        if (pts == null || pts == undefined) {
            return this
        }
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
    mount_d(pts: string | any[]) {
        this.on_mount_call["set_d"] = [pts]
        return this
    }
    render_option(): void {
        this.set_d(this.option.value)
        this.set_color(this.option.data.color)
    }
    set_color(color: string) {
        if (color == null || color == undefined) {
            return this
        }
        return this.set_style({ stroke: color })
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

    with_arrow_start() {
        return this.set_attr("marker-start", Defs.marker_id(ARROW_KEY, ARROW_START))
    }
    with_arrow() {
        return this.set_attr("marker-end", Defs.marker_id(ARROW_KEY, ARROW_END))
    }
}
export function line() {
    return new Line()
}