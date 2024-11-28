import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, Row, node, Select, select, Pre, pre,
    line, gnode, GNode, button, progress, div, input, Input, Progress, DivFactory, row1, row2,
    text_area, TextArea, Util, web_socket, Data
} from "../../base/components/export";
export class Game extends Div {
    game_id: string
    room_id: string
    user_id: string

    do_msg(n: Node) {

    }
    init_game() {

    }
    post(tp: string, data: any) {
        web_dom.post('/app/yly/game/gm/do', {
            room_id: this.room_id,
            game_id: this.game_id,
            user_id: this.user_id,
            tp, data
        }, () => {

        })
    }
    on_mount(): void {
        this.room_id = web_dom.get_param("room_id")
        if (!this.room_id) {
            return
        }
        web_socket.login((user_id: string) => {
            this.user_id = user_id
            this.post('login', {})
            this.init_game()
        })
        web_socket.sub(this.room_id, (data: Node) => {
            this.do_msg(data)
        })


    }

}
