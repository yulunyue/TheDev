import {
    Column, Row, Div, Constant, Node, web_dom, oj_to_node, to_node, Search, Container,
    Button,
    Input,
    FormRow,
    Data
} from "../base/components/export";
export class Talk extends Row {
    msgs: Row
    send_msg: Input
    send_btn: Button
    init_style(): void {
        this.msgs.set_style({ height: 500 })
    }
    init_node(): void {
        this.msgs = new Row()
        this.send_msg = new Input().set_value("test")
        this.send_btn = new Button().set_html("发送")
        this.add_childs([
            this.msgs,
            new Column().add_childs([
                this.send_msg,
                this.send_btn
            ])
        ])
    }
    init_event(): void {
        this.send_btn.on_click(this.send.bind(this))
    }
    send() {
        Data.get_user_name(() => {

        })
    }
}
export default function () {
    return new Talk()
}