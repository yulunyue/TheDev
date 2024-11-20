import { Line, line } from "../line";
import { Node, to_node } from "../../../web/cls";
import { Text, text } from "./div_text";
import { GNode, gnode } from "../gnode";
import { Svg, svg } from "../svg";
export class TreeNode extends GNode {
    line: Line
    text: Text
    parent: TreeNode
    height1: number
    height2: number
    nodes: TreeNode[]
    init_node(): void {
        this.nodes = []
        this.line = line().with_arrow()
        this.text = this.add_child(text().on_change(() => this.on_text_change()))
        this.parent = null
    }
    on_text_change() {
        let h = this.text.get_height()
        this.line.set_dst(this.option.data.pos.y - h / 2 - 2, this.option.data.pos.x)
        for (var i = 0; i < this.nodes.length; i++) {
            this.nodes[i].line.set_src(this.option.data.pos.y + h / 2 + 2, this.option.data.pos.x)
        }

    }
    add_node(c: TreeNode) {
        this.nodes.push(c)
        c.parent = this
        return c.line
    }
    set_option(option: Node) {
        this.set_pos(option.data.pos.x, option.data.pos.y)
        this.option = option
        this.text.set_html(option.get_title())
        return this
    }

}
export class Tree extends Svg {
    max_xy: any
    g: GNode
    add_dfs_childs(nodes: any, depth: any) {
        console.log(nodes, depth)
    }
    init_node(): void {
        this.g = this.add_child(new GNode())
    }
    render_option() {
        this.max_xy = this.option.init_layout()
        this.draw()
    }
    calc_pos(x: number, y: number) {
        let h = Math.min(1 / this.max_xy.y * this.get_height(), 150)
        let w = Math.min(1 / this.max_xy.x * this.get_width(), 210)
        let margin_left = (this.get_width() - w * this.max_xy.x) / 2
        let margin_top = (this.get_height() - h * this.max_xy.y) / 2 - 30
        return {
            x: margin_left + x * w,
            y: margin_top + y * h
        }
    }
    draw() {
        if (!this.get_width() || !this.get_height() || !this.max_xy) {
            return
        }
        console.warn(this.get_width(),this.get_height(),this.max_xy)
        this.g.clear()
        var dfs = (node: Node, p: Node) => {
            node.data.node = new TreeNode()
            node.data.pos = this.calc_pos(node.x, node.y)
            node.data.node.set_option(node)
            this.g.add_child(node.data.node)
            if (p) {
                this.g.add_child(p.data.node.add_node(node.data.node))
            }
            for (var i = 0; i < node.childs.length; i++) {
                dfs(node.childs[i], node)
            }
        }
        dfs(this.option, null)
    }
    on_mount(): void {
        this.draw()
    }
}
export function tree() {
    return new Tree()
}