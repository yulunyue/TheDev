import { GNode } from "../gnode";
import { Line } from "../line";
import { SvgNode } from "../svg";
import { Circle } from "../circle";
import { Node } from "../../../web/cls";
import { Text, text } from "../text";
export class ListNode extends GNode {
    text: Text
    init_node(): void {
        this.text = this.add_child(text())
    }
    set_index(i: number) {
        return this
    }
    render_option(): void {
        this.text.set_html(this.option.title)
    }
}
export class ListView extends SvgNode {
    g: GNode
    init_node(): void {
        this.g = this.add_child(new GNode())
    }
    draw_child() {

    }
    draw() {
        this.g.clear().add_childs(
            this.option.data.map(
                (v: Node, i: number) => new ListNode().set_option(v)
            )
        )
    }
    on_mount(): void {

    }
    render_option(): void {
        // this.draw()
    }

}
export function list_view() {
    return new ListView()
}