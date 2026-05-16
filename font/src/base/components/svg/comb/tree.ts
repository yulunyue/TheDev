import { Line } from "../line";
import { Node, to_node } from "../../../web/cls";
import { Text, text } from "../comb/div_text";
import { GNode } from "../gnode";
import { SvgNode } from "../svg";
export class TreeNode extends GNode {
    line!: Line
    text!: Text
    parent: TreeNode | null = null
    height1: number = 0
    height2: number = 0
    nodes: TreeNode[] = []
    init_node(): void {
        this.line = new Line().with_arrow()
        this.text = this.add_child(text().on_change(() => this.on_text_change()))
    }
    on_text_change() {
        let h = this.text.get_height()
        this.line.set_dst(this.option.data.y - h / 2 - 2, this.option.data.x)
        for (var i = 0; i < this.nodes.length; i++) {
            this.nodes[i].line.set_src(this.option.data.y + h / 2 + 2, this.option.data.x)
        }

    }
    add_node(c: TreeNode) {
        this.nodes.push(c)
        c.parent = this
        return c.line
    }
    render_option() {
        this.set_pos(this.option.data.y, this.option.data.x)
        this.text.set_text(this.option.data)
        return this
    }

}
export class Tree extends SvgNode {
    max_xy: any
    g: GNode
    add_dfs_children(nodes: any, depth: any) {
        console.log(nodes, depth)
    }
    init_node(): void {
        this.g = this.add_child(new GNode())
    }
    render_option() {
        this.max_xy = this.option.init_tree_layout()
        this.draw()
    }
    calc_pos(x: number, y: number) {

        let h = Math.min(1 / this.max_xy.y * this.get_height(), 100)
        let w = Math.min(1 / this.max_xy.x * this.get_width(), 140)
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
        this.g.clear()
        var dfs = (node: Node, p: Node | null) => {
            node.data.node = new TreeNode()
            node.set_data(this.calc_pos(node.x, node.y))
            node.data.node.set_option(node)
            this.g.add_child(node.data.node)
            if (p) {
                this.g.add_child(p.data.node.add_node(node.data.node))
            }
            for (var i = 0; i < node.children.length; i++) {
                dfs(node.children[i], node)
            }
        }
        if (this.option.title) {
            dfs(this.option, null)
        } else {
            this.option.children.map((v => {
                dfs(v, null)
            }))
        }
    }
    on_mount(): void {
        this.draw()
    }
}
export function tree() {
    return new Tree()
}