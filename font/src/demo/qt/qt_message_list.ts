import { Div } from "../../base/components/export"
import QtMessageItem from "./qt_message_item"

export class QtMessageList extends Div {
    child_items: any[] = []

    init_style(): void {
        this.set_style({
            height: "100%",
            backgroundColor: "#34495e",
            overflow: "hidden",
            padding: 10,
            display: "flex",
            flexDirection: "column",
        })
    }

    render_mock_data(): void {
        const statuses = ["running", "completed", "failed", "blocked", "idle", "busy"]
        for (let i = 0; i < 20; i++) {
            this.add_message({
                key: `mock_${i.toString().padStart(2, '0')}`,
                title: `Mock Message Title ${i}`,
                data: { status: statuses[i % statuses.length] }
            })
        }
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