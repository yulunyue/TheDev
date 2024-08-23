import { Div, Svg, svg, Constant, Node } from "../base/components/export";

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
        root.dfs((n: Node, height: number, width: number) => {

        }, 0, 0)
    }
    test() {
        this.draw_tree_view(Constant.MOCK_NODE_3_5)
    }
}
export default function () {
    return new Algo().init().test()
}