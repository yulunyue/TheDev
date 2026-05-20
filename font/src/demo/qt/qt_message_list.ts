import { Div } from "../../base/components/export"
import QtMessageItem from "./qt_message_item"

export class QtMessageList extends Div {
    child_items: any[] = []

    init_style(): void {
        this.set_style({
            flex: "1",
            backgroundColor: "#34495e",
            overflow: "auto",
            padding: 10,
            display: "flex",
            flexDirection: "column",
        })
    }

    add_message(msg: any): void {
        let idx = this.child_items.findIndex(c => c.key === msg.key)
        if (idx >= 0) {
            this.child_items.splice(idx, 1)
        }
        this.child_items.unshift(msg)
        this.set_children(this.child_items, (data: any) => new QtMessageItem().set_option(data))
    }
}

export default QtMessageList