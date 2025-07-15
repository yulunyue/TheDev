import { Game } from "./base"
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, Row, node, Select, select, Pre, pre,
    line, gnode, GNode, button, progress, div, input, Input, Progress, DivFactory, row1, row2,
    text_area, TextArea, Util, web_socket, Data, Button, mera_util, MeraGraph,
    Grid,
    to_node
} from "../../base/components/export";
let W = 7
let H = 7
let STATE_STR = ['-', 'O', 'X']
function get_board(state?: any) {
    let ret = []
    for (var i = 0; i < H; i++) {
        for (var j = 0; j < W; j++) {
            ret.push(node().set_option({
                y: i,
                x: j,
                title: i == H - 1 ? '*' : '-'
            }))
        }
    }
    return ret

}
class GameConnectFour extends Game {
    m: Grid

    init_node(): void {
        this.game_id = 'CfGame'
        this.m = new Grid().set_option(to_node({
            x: W,
            y: H,
        }).set_childs(
            get_board()
        ))
        this.full().set_style({
            position: "fixed"
        }).add_child(this.m)
    }
    init_event(): void {
        this.m.do_select((v: any) => {
            this.hander_select(v)
        })
    }
    init_game(): void {
        // this.post("reset")
    }
    hander_select(op: Node) {
        console.log(op)
    }
    do_msg(n: Node): void {
        // this.m.set_option(n)
        console.log(n)
    }



}
export default function () {
    return new GameConnectFour()
}