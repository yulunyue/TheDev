import {
    Div, Svg, svg, Constant, Node,
    svg_node_factory, line, gnode, GNode, button, progress, div,input,Input
} from "../base/components/export";

import { SegTree } from "../base/algo/seg_tree";
class Algo extends Div {
    svg_node: GNode
    line_proress: GNode
    input_line:Input
    init_style(): void {
        this.full()
    }
    init_node() {
        this.svg_node = gnode()
        this.line_proress = progress()
        this.input_line = input().set_width(Constant.INPUT_NUMBER_WIDTH)
        this.add_childs([
            svg().add_childs([this.svg_node]).set_size(1),
            div().add_childs([
                svg().add_childs([this.line_proress]).set_size(1),            
                button().set_html("<<"),
                this.input_line,
                button().set_html("go"),
                button().set_html(">>"),
                button().set_html("setting"),
                button().set_html("run")
            ]).set_height(Constant.DEFAULT_LINE_HEIGHT)
        ]).flex_horizontal_layout()
    }

    test() {

    }
    on_mount() {
        this.test()
    }
}
export default function () {
    return new Algo()
}