
import {
    Div, Constant, Node, web_dom, oj_to_node, Form, to_node, Search, Container,
    Button,
    Svg,
    Grid,
    Row
} from "../../base/components/export";
export class Chess extends Row {
    g: Grid
    init_style(): void {
        super.init_style()
        this.full()
        this.g.set_height(300)
    }
    init_node(): void {
        this.g = new Grid().set_option({

        })
        this.add_childs([
            this.g
        ])
    }
}
export default function () {
    return new Chess()
}