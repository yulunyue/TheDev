import { Game } from "./base"
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, Row, node, Select, select, Pre, pre,
    line, gnode, GNode, button, progress, div, input, Input, Progress, DivFactory, row1, row2,
    text_area, TextArea, Util, web_socket, Data, Button, mera_util, MeraGraph
} from "../../base/components/export";
class GameAb extends Game {
    m: MeraGraph
    init_node(): void {
        this.game_id = 'AbGame'
        this.m = this.full().set_style({
            position: "fixed"
        }).add_child(mera_util().on_select((s: any) => this.select_node(s)))
    }
    init_game(): void {
        // this.post("reset")

    }
    select_node(name: string) {
        this.post("open", { key: name })
    }
    do_msg(n: Node): void {
        this.m.set_option(n)
    }



}
export default function () {
    return new GameAb()
}