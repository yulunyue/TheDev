import { Game } from "./base"
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, Row, node, Select, select, Pre, pre,
    line, gnode, GNode, button, progress, div, input, Input, Progress, DivFactory, row1, row2,
    text_area, TextArea, Util, web_socket, Data, Button,mera_util,MeraGraph
} from "../../base/components/export";
class GameAb extends Game {
    m:MeraGraph
    init_node(): void {
        this.game_id = 'AbGame'
        this.m=this.full().add_child(mera_util())
    }
    init_style(): void {

    }

    do_player_msg(player_self: Node, players: Node[], option: Node) {
        console.error(option)
    }



}
export default function () {
    return new GameAb()
}