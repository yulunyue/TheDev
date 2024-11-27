import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, Row, node, Select, select, Pre, pre,
    line, gnode, GNode, button, progress, div, input, Input, Progress, DivFactory, row1, row2,
    text_area, TextArea, Util, web_socket, Data
} from "../../base/components/export";
export class Game extends Div {
    game_id: string
    room_id: string
    div1: Div
    div2: Div
    init_node(): void {
        this.div1 = div()
        this.div2 = div().set_size(1)
        this.add_child(div().add_childs([
            this.div1,
            this.div2,
        ]).set_flex_style(
            Constant.VERTICAL
        ))
    }
    do_msg(n: Node) {
        console.warn(n)
    }
    init_game() {

    }
    on_mount(): void {
        this.room_id = web_dom.get_param("room_id")
        if (!this.room_id) {
            return
        }
        web_socket.sub(this.room_id, (data: Node) => {
            this.do_msg(data)
        })
        this.init_game()
    }

}
