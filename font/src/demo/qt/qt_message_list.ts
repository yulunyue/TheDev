import { Div } from "../../base/components/export"
import QtMessageItem from "./qt_message_item"

export class QtMessageList extends Div {
    show_keys: string[] = []



    init_style(): void {
        this.set_style({
            flex: 1,
            backgroundColor: "#34495e",
            overflow: "auto",
            padding: 10,
            display: "flex",
            flexDirection: "column",
        })
    }

    render_option(): void {
        this.set_children(this.option.children, this.add_displayed_item.bind(this))
    }
    add_displayed_item(data: any) {
        return new QtMessageItem().set_option(data)
    }

    add_message(msg: any): void {
        if (this.children_map[msg.key]) {
            this.children_map[msg.key].set_option(msg)
        }
    }
}

export default QtMessageList