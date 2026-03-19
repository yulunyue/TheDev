
import {
    Div, Constant, Node, web_dom, oj_to_node, Form, to_node, Search, Container,
    Button,
    Svg,
    Grid,
    Row,
    Pre,
    Column
} from "../../base/components/export";
export class Chess extends Column {
    g: Grid
    left: Div
    right: Div
    middle: Div
    top_control: Div
    init_style(): void {
        super.init_style()
        this.full().set_center()
        this.left.set_size(1)
        this.right.set_size(1)
        this.middle.set_width(400)
        this.g.set_height(400)
    }
    init_node(): void {
        this.g = new Grid().set_option({
        })
        this.left = new Div()
        this.right = new Div()
        this.middle = new Div().add_childs([
            this.g
        ])
        this.add_childs([
            this.left,
            this.middle,
            this.right
        ])
    }
}
export default function () {
    return new Chess()
}