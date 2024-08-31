import { Div, Svg, svg, Constant, Node, 
    svg_node_factory, line ,gnode,GNode
} from "../base/components/export";
import { SegTree } from "../base/algo/seg_tree";
class Algo extends Div {
    svg_node: GNode
    init_style(): void {
        this.full()
    }
    init() {
        this.svg_node = gnode()
        
        return this.add_childs([
            svg().full().add_child(this.svg_node)
        ])
    }
    draw_tree_view(root: Node) {
        let w = this.get_width()
        let h = this.get_height()
        this.svg_node.clear()
        let nodes: Node[] = []
        let store_tmp = {}
        let max_depth = 0
        root.dfs((n: Node, i: number, j: number) => {
            if (!store_tmp[i]) {
                store_tmp[i] = 0
            }
            store_tmp[i] += 1
            max_depth = i > max_depth ? i : max_depth
            n.type = n.type || 'text'
            n.data = { i: i, j: store_tmp[i] - 1, r: 5 }
            nodes.push(n)
        }, 0, 0)
        for (var i = 0; i < nodes.length; i++) {
            nodes[i].data.y = h * ((nodes[i].data.i + 0.5) / (max_depth + 1))
            nodes[i].data.x = w * ((nodes[i].data.j + 0.5) / store_tmp[nodes[i].data.i])
            let n = svg_node_factory(nodes[i])
            this.svg_node.add_child(n)
            if (nodes[i].parent) {
                this.svg_node.add_child(line().set_d([
                    { x: nodes[i].parent.data.x, y: nodes[i].parent.data.y },
                    { x: nodes[i].data.x, y: nodes[i].data.y }
                ]).with_arrow())
            }

        }
    }
    test() {
        this.draw_tree_view(new SegTree().build(1,0,31))
    }
    on_mount() {
        this.test()
    }
}
export default function () {
    return new Algo().init()
}