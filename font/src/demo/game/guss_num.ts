import { Game } from "./base"
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, Row, node, Select, select, Pre, pre,
    line, gnode, GNode, button, progress, div, input, Input, Progress, DivFactory, row1, row2,
    text_area, TextArea, Util, web_socket, Data, Button,
} from "../../base/components/export";
class GaussPlayer extends Div {
    input: Input
    name: Div
    result: Div
    parent: GussNum
    btn: Button
    btn_type: string
    init_node(): void {
        this.name = div()
        this.input = input()
        this.result = div()
        this.btn = button().set_html('猜测')
        this.btn_type = 'gauss_num'
        this.add_childs([
            this.name,
            div().add_childs([this.input]),
            div().add_childs([this.btn]),
            this.result
        ])
    }
    set_self() {
        this.btn.set_html('设置')
        this.btn_type = 'set_num'
        return this
    }
    init_style(): void {
        this.set_size(1).set_center()
    }
    init_event(): void {
        this.btn.click(() => { this.action() })
    }
    render_option(): void {
        this.name.set_html(this.option.key + '[' + (this.option.value ? '已设置' : '未设置') + ']')
        this.result.clear().add_childs(this.option.data.records.map((v: any) => div().set_html(v)))
    }
    action() {
        this.option.data.action(this.btn_type, this.input.get_value(), this.option.key)
    }
}
class GussNum extends Game {
    row2: Pre
    player: GaussPlayer
    record: Div
    init_node(): void {
        this.game_id = 'GusNum'
        this.row2 = this.add_child(div().set_height(240))
        let rule = pre().add_childs([
            '猜数字游戏规则:',
            '该游戏有多名玩家以及一名ai玩家',
            '游戏开始前',
            '每名玩家会选择四位数字,AI玩家会随机选择',
            '所有玩家轮流选择一名其它玩家B,输入四位数字',
            '如果B选择的数字和玩家猜测的数字相同，该玩家胜利，游戏结束',
            '否则系统会输出两个数字表示与玩家B选择数字的区别',
            '下一个玩家继续猜测'
        ].map(v => div().set_html(v)))
        this.player = new GaussPlayer().set_self()
        this.record = div()
        this.add_childs([
            div().add_childs([
                rule,
                this.player,
                div().add_childs([
                    div().set_html('房间公告'),
                    this.record
                ])
            ]).set_size(1),
            this.row2
        ]).flex_horizontal_layout()
    }
    init_style(): void {

    }

    do_player_msg(player_self: Node, players: Node[], option: Node) {
        let action = (tp: string, value: string, user_id2: string) => { this.post(tp, { value, user_id2 }) }
        player_self.data.action = action
        players.map(v => {
            v.data.action = action
        })
        this.player.set_option(player_self)
        this.row2.update_option(new Node().set_childs(players), GaussPlayer)
        this.record.clear().add_childs(option.data.records.map((v: any) => div().set_html(v)))
    }



}
export default function () {
    return new GussNum()
}