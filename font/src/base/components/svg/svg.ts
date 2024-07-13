import { Div } from "../dom/div"
import { Defs, defs } from "./defs"
import { line } from "./line"
import { circle } from "./circle"
import { GNode } from "./gnode"
import { Text, text } from "./text"
import web_dom from "../../web/web_dom"
export class Svg extends GNode {
    constructor() {
        super("svg", "div")
    }
    set_size(w: number, h: number): this {
        this.set_attr("width", w).set_attr("height", h)
        return this
    }
    init_node(): void {
        this.set_attr("shape-rendering", "geometricPrecision")
        this.add_child(defs())
    }
    init_style(): void {
        this.set_style({
            width: 1,
            height: 1
        })
    }
    set_backgroud_grid() {

    }
}
export function svg_dev() {
    let c = circle().set_pos(100, 100).set_r(10)
    function loop() {
        let x = c.get_x() + 1
        if (x > 200) { x = 100 }
        c.set_x(x)
        return 0
    }
    console.log(c)
    web_dom.add_task("svg_dev", loop, 1)
    return new Svg().add_childs([
        text().set_pos(20, 30).set_html("xxx"),
        line().set_d("M150 5 L75 200 L225 200 Z"),
        line().mount_d([{ x: 0, y: 0 }, { x: 1, y: 1 }]),
        c
    ])
}