import { Line, line } from "../line";
import { Node } from "../../../web/cls";
import { Text, text } from "../text";
import { GNode, gnode } from "../gnode";
export class TreeNode extends GNode {
    lines: Line[]
    text: Text
    parent: TreeNode
    init_node(): void {
        this.lines = []
        this.text = this.add_child(text())
        this.parent = null
    }
    add_node(c: TreeNode) {
        return line().set_d([
            { x: this.option.data.pos.x, y: this.option.data.pos.y },
            { x: c.option.data.pos.x, y: c.option.data.pos.y }
        ]).with_arrow()
    }
    set_option(option: Node) {
        this.set_pos(option.data.pos.x, option.data.pos.y)
        this.option = option
        this.text.set_html(option.get_title())
        return this
    }

}
export class Tree extends GNode {
    width: number
    height: number
    margin_top: number = 10
    margin_left: number = 30
    max_xy: any
    set_option(option: Node): this {
        this.max_xy = option.init_layout()
        this.option = option
        this.draw()
        return this
    }
    calc_pos(x: number, y: number) {
        return {
            x: this.margin_left + x / this.max_xy.x * (this.width - this.margin_left * 2),
            y: this.margin_top + y / this.max_xy.y * (this.height - this.margin_top * 2)
        }
    }
    draw() {
        if (!this.width || !this.height || !this.option) {
            return
        }
        this.clear()
        var dfs = (node: Node, p: Node) => {
            node.data.node = new TreeNode()
            node.data.pos = this.calc_pos(node.x, node.y)
            node.data.node.set_option(node)
            this.add_child(node.data.node)
            if (p) {
                this.add_child(p.data.node.add_node(node.data.node))
            }
            for (var i = 0; i < node.childs.length; i++) {
                dfs(node.childs[i], node)
            }
        }
        dfs(this.option, null)
    }
    on_mount(): void {
        this.width = this.parent.get_width()
        this.height = this.parent.get_height()
        this.draw()
    }
}
export function tree() {
    return new Tree
}