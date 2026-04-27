import { FlexColumn } from "./base/row"
import { Div } from "./base/div"
import { DivFactory } from "./base/div_factory"
import { Constant, web_socket } from "../export"
export class ListContainer extends Div {
    init_style(): void {
        super.init_style()
        this.set_style({
            overflow: "auto",

        })
    }
    add_node(option: any) {
        let d = DivFactory.new_div(
            option.type, option.key
        ).set_option(option)
        this.add_child(d)
        this.scroll_to_bottom()
        return this
    }
    add_msg(msg: any) {

        if (typeof msg == "string") {
            this.add_node({ value: msg, type: Constant.DOM_TYPE_TITLE })
        }
    }
    sub(topic: string) {
        web_socket.sub(topic, (data: any) => {

            this.add_msg(data)
        })
    }

}