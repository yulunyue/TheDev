import { Div } from "../dom/div"
import { Defs, defs } from "./defs"
import { line } from "./line"
import { circle } from "./circle"
import { GNode } from "./gnode"
import { grid } from "./comb/grid"
import { Text, text } from "./text"
import { Node } from "../../web/cls"
import web_dom from "../../web/web_dom"
export class Svg extends GNode {
    constructor() {
        super("svg")
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
export function svg() {
    return new Svg()
}
export function svg_node_factory(n: Node) {
    return {
        circle,
        text
    }[n.type](

    ).set_option(n)
}
export function svg_dev() {
    let c = circle().set_pos(10, 10).set_r(10)
    function loop() {
        let x = c.get_x() + 1
        if (x > 200) { x = 100 }
        c.set_x(x)
        return 0
    }
    web_dom.add_task("svg_dev", loop, 1)
    return svg().add_childs([
        text().set_pos(4, 4).set_html("xxx"),
        // line().set_d("M0 5 L5 10 L30 0 Z"),
        line().mount_d([
            { x: 0, y: 0 },
            { x: 0, y: 1 },
            { x: 1, y: 1 },
            { x: 1, y: 0 }
        ]),
        grid(),
    ])
}