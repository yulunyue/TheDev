import { Div, Svg, svg, Constant, Node, 
    svg_node_factory, line ,gnode,GNode,Layout
} from "../base/components/export";
import { SegTree } from "../base/algo/seg_tree";
class Algo extends Layout {
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
   
    test() {
        
    }
    on_mount() {
        this.test()
    }
}
export default function () {
    return new Algo().init()
}