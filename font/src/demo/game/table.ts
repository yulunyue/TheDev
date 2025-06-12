import { Game } from "./base"
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, Row, node, Select, select, Pre, pre,
    line, gnode, GNode, button, progress, div, input, Input, Progress, DivFactory, row1, row2,
    text_area, TextArea, Util, web_socket, Data, Button, mera_util, MeraGraph, ListUi, Table, Ct,
} from "../../base/components/export";
class GameTable extends Game {
    table_ui: Table
    init_node(): void {
        this.game_id = 'TbGame'
        this.table_ui = this.add_child(new Table())
    }
    init_game(): void {
        // this.post("reset")

    }

    do_msg(n: Node): void {

    }



}
export default function () {
    return new GameTable()
}