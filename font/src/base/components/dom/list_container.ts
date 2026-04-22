import { Row } from "./base/row"
import { DivFactory } from "./base/div_factory"
import { web_socket } from "../export"
export class ListContainer extends Row {
    add_node(option: any) {
        let d = DivFactory.new_div(
            option.type, option.key
        ).set_option(this.option)
        this.add_child(d)
        this.scroll_to_bottom()
        return this
    }
    add_msg(msg: any) {
        if (typeof msg == "string") {
            this.add_node({ value: msg, type: "pre" })
        }
    }
    sub(topic: string) {
        web_socket.sub(topic, (data: any) => {
            this.add_msg(data)
        })
    }

}