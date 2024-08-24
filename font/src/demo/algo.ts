import { Div, Svg, svg, Constant, Node, svg_node_factory, line } from "../base/components/export";

class Algo extends Div {
    svg_node: Svg
    init_style(): void {
        this.full()
    }
    init() {
        this.svg_node = svg().full()
        return this.add_childs([
            this.svg_node
        ])
    }
    draw_tree_view(root: Node) {
        let w = this.get_width()
        let h = this.get_height()
        console.log(w, h)
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
        this.draw_tree_view(Constant.MOCK_NODE_3_5)
    }
    on_mount() {
        this.test()
    }
}
export default function () {
    return new Algo().init()
}