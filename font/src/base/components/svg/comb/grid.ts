import { GNode, gnode } from "../gnode";
import { line } from "../line";
import { SvgNode } from "../svg";
import { circle } from "../circle";
import { Rect, rect } from "../rect";
export class Grid extends SvgNode {
    g: GNode
    init_node(): void {
        this.g = this.add_child(new GNode())
    }
    draw_child() {
        for (var i = 0; i < this.option.childs.length; i += 1) {
            // this.add_child()
        }
    }
    draw() {
        if (!this.get_width() || !this.get_height()) {
            return
        }
        this.g.clear()
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