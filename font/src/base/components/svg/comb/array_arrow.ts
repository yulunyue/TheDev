import { SvgNode } from "../svg";
import { Text } from "./div_text"
import { GNode } from "../gnode";
import { Rect } from "../rect";
import { Line } from "../line";
export class Grid extends SvgNode {
    texts: Map<string, Text>
    arrows: Map<string, Line>
    g: GNode
    init_node(): void {
        this.g = new GNode()
        this.add_children([
            this.g
        ])
    }
    render_option(): void {
        this.g.clear()
        this.texts = new Map()
        this.arrows = new Map()
        for (var i = 0; i < this.option.children.length; i++) {
            let o = this.option.children[i]
            this.texts[o.key] = new Text().set_option(o)
            this.g.add_child(this.texts[o.type])
        }
        let arrows = this.option.data.arrows || []
        for (var i = 0; i < arrows.length; i++) {
            let o = arrows[i]
            this.arrows[o.key] = new Line().set_option(o)
            this.g.add_children(this.arrows[o.key])
        }
    }
}