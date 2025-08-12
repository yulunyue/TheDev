import { GNode } from "../gnode";
import { Line } from "../line";
import { text, Text } from "./div_text";
import { SvgNode } from "../svg";
import { Circle } from "../circle";
import { Rect, Polygon } from "../rect";
const NODE_GEN = {

}
export class Grid extends SvgNode {
    g: GNode
    default_cell_width = 40
    default_cell_height = 40
    init_node(): void {
        this.g = this.add_child(new GNode())
    }
    draw_child() {
        this.g.clear()
        for (var i = 0; i < this.option.childs.length; i += 1) {
            let op = this.option.childs[i]
            let fun = NODE_GEN[op.type]
            if (!fun) {
                fun = text
            }
            let el: Text = fun().set_option(op)
            el.set_width(this.default_cell_width).set_height(this.default_cell_height)
            el.set_x(op.x * this.default_cell_width).set_y(op.y * this.default_cell_height)
            this.g.add_child(el)
        }
    }
    draw() {
        if (!this.get_width() || !this.get_height()) {
            return
        }
        this.draw_child()
    }

    on_mount(): void {
        this.draw()
    }
    render_option(): void {
        this.draw()
    }

}
export function grid() {
    return new Grid()
}