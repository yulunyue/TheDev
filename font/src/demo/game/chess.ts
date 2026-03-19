
import {
    Div, Constant, Node, web_dom, oj_to_node, Form, to_node, Search, Container,
    Button, Progress,
    Svg,
    Grid,
    Row,
    Pre,
    Column,
} from "../../base/components/export";
export class Chess extends Column {
    g: Grid
    left: Div
    right: Div
    middle: Div
    top_control: Div
    pro: Progress
    top_form: Form
    chess_width: number
    init_style(): void {
        super.init_style()
        this.full().set_center()
        this.left.set_size(1)
        this.right.set_size(1)
        this.chess_width = 300
        this.middle.set_width(this.chess_width)
        this.g.set_height(this.chess_width)
    }
    init_node(): void {
        this.g = new Grid().set_option({
        })
        this.top_form = new Form()
        this.pro = new Progress()
        this.left = new Div()
        this.right = new Div()
        this.middle = new Div().add_childs([
            this.top_form,
            this.g,
            this.pro,
        ])
        this.add_childs([
            this.left,
            this.middle,
            this.right
        ])
    }
    render(): void {
        this.top_form.set_uri("/game/chess/bd")
    }

}
export default function () {
    return new Chess()
}