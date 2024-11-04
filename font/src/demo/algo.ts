import {
    Div, Svg, svg, Constant, Node,
    svg_node_factory, line, gnode, GNode, button, progress, div, input, Input
} from "../base/components/export";
class Algo extends Div {
    div: Div

    init_style(): void {
        this.full()
    }
    init_node() {
        this.div = div()
        this.add_childs([
            this.div.set_size(1),
            div().add_childs([
                progress().set_size(1),
                button().set_html("setting"),
                button().set_html("run")
            ]).set_height(Constant.DEFAULT_LINE_HEIGHT)
        ]).flex_horizontal_layout()
    }
    set_option(option: Node): this {
        this.div.clear().add_grid_childs(
            option.childs.map(v => svg_node_factory(v))
        ).abs_veritcal_layout()
        return this
    }
    test() {
        this.set_option(new Node())
    }
    on_mount() {
        this.test()
    }
}
export default function () {
    return new Algo()
}