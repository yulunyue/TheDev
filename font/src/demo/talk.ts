import {
    FlexRow, FlexColumn, Div, Constant, Node, web_dom, oj_to_node,
    to_node, Search, Container,
    Button,
    Input,
    FormRow,
    Data,
    web_socket,
    Ct,
    Pre,
} from "../base/components/export";
export class Talk extends FlexColumn {
    msgs: Div
    send_msg: Input
    send_btn: Button
    init_style(): void {
        this.msgs.set_style({ overflow: "auto" }).set_size(1)
        this.full()
        super.init_style()
    }
    init_node(): void {
        this.msgs = new Div()
        this.send_msg = new Input().set_value("test")
        this.send_btn = new Button().set_html("发送")
        this.add_children([
            this.msgs,
            new FlexRow().add_children([
                this.send_msg,
                this.send_btn
            ])
        ])
    }
    init_event(): void {
        this.send_btn.on_click(this.send.bind(this))
    }
    send() {
        Data.get_user_name((username: string) => {
            web_socket.send_data(Ct.METHOD_SEND_TO, {
                dst: username,
                msg: this.send_msg.get_value()
            })
        })
    }
    send_hock(tp: string, value: any) {
        this.msgs.add_child(new Pre().set_value({ method: "send_hock", tp, value }))
        this.msgs.scroll_to_bottom()
    }
    recv_hock(data: any) {
        this.msgs.add_child(new Pre().set_value({ method: "recv_hock", data }))
        this.msgs.scroll_to_bottom()
    }
    render(): void {
        web_socket.send_hock = this.send_hock.bind(this)
        web_socket.recv_hock = this.recv_hock.bind(this)
    }

}
export default function () {
    return new Talk()
}