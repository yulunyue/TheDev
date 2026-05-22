import { Div, Constant } from "../../base/components/export"
import web_socket from "../../base/web/web_socket"
import QtDragBar from "./qt_drag_bar"
import QtMessageList from "./qt_message_list"


export class QtMain extends Div {
    message_list: QtMessageList

    init_node(): void {
        this.add_child(new QtDragBar())
        this.message_list = new QtMessageList()
        this.add_child(this.message_list)
    }

    init_style(): void {
        this.set_style({
            width: "100%",
            height: "100%",
            display: "flex",
            flexDirection: "column",
        })
    }

    render(): void {
        web_socket.sub(Constant.TOPIC_MSG_QT, (msg: any) => {
            this.message_list.add_message(msg)
        })
    }
}

export default function () {
    return new QtMain()
}