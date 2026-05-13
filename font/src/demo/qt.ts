import { Div, web_dom, Constant } from "../base/components/export"
import web_socket from "../base/web/web_socket"
import QtDragBar from "./qt_drag_bar"
import QtMessageList from "./qt_message_list"

const QT_USER_NAME = "yly_opencode"

export class QtMain extends Div {
    message_list: QtMessageList

    init_node(): void {
        this.add_child(new QtDragBar())
        this.message_list = new QtMessageList()
        this.add_child(this.message_list)
    }

    init_style(): void {
        this.set_style({
            width: 1,
            height: 1,
            display: "flex",
            flexDirection: "column",
        })
    }

    init_event(): void {
        web_dom.set_local(Constant.username, QT_USER_NAME)

        web_socket.sub(Constant.TOPIC_QT_CONFIG_UPDATE, (config: any) => {
            this.message_list.set_config(config)
        })

        web_socket.sub(Constant.TOPIC_MSG_QT, (msg: any) => {
            this.message_list.add_message(msg)
        })

        web_dom.post("/app/manage/get_qt_show_config", {}, (data: any) => {
            this.message_list.set_config(data.value)
        })
    }
}

export default function () {
    return new QtMain()
}