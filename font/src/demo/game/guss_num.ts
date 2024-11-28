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
    init_node(): void {
        this.name = div()
        this.input = input()
        this.result = div()
        this.btn = button()
        this.add_childs([
            this.name,
            div().add_childs([this.input]),
            div().add_childs([this.btn]),
            this.result
        ])
    }
    init_style(): void {
        this.set_size(1).set_style({
            textAlign: "center",
            margin: 30
        })
    }
    init_event(): void {
        this.btn.click(() => { this.action() })
    }
    render_option(): void {
        this.name.set_html(this.option.key + '[' + (this.option.value ? '已设置' : '未设置') + ']')
        if (!this.parent) {
            return
        }
        this.btn.set_html(this.option.key == this.parent.user_id ? "设置" : "猜测")
        this.result.set_html(JSON.stringify(this.option.data))
    }
    action() {
        this.parent.action(this.option.key == this.parent.user_id ? "set_num" : "gauss_num", this.input.get_value(), this.option.key)
    }
}
function gauss_p() {
    return new GaussPlayer()
}
class GussNum extends Game {

    init_node(): void {
        this.game_id = 'GusNum'

    }
    init_style(): void {
        this.set_style_flex2(Constant.HORIZONTAL).set_style({
            width: 1,
            height: 1
        })
    }
    action(tp: string, value: string, user_id2: string) {
        this.post(tp, { value, user_id2 })
    }
    do_msg(option: Node) {
        console.log(option)
        // this.add_child(gauss_p())
        this.update_option(option, gauss_p)
    }



}
export default function () {
    return new GussNum()
}