import { Div } from "../base/components/export"

export class QtMessageItem extends Div {
    key: string = ""
    data: any = null

    init_style(): void {
        this.set_style({
            padding: 8,
            marginBottom: 4,
            borderRadius: 4,
            fontSize: 12,
        })
    }

    set_msg(data: any): this {
        this.key = data.key
        this.data = data
        let displayMsg = `${data.user} - oc_${data.key} ${data.title}`
        this.set_html(displayMsg)

        let colorMap: any = {
            "running": { backgroundColor: "#3498db", color: "#fff" },
            "completed": { backgroundColor: "#27ae60", color: "#fff" },
            "failed": { backgroundColor: "#c0392b", color: "#fff" },
            "blocked": { backgroundColor: "#e67e22", color: "#fff" },
        }
        let style = colorMap[data.status] || { backgroundColor: "#2c3e50", color: "#ecf0f1" }
        this.set_style(style)
        return this
    }
}

export class QtMessageList extends Div {
    show_keys: string[] = []
    all_messages: Map<string, any> = new Map()
    displayed_items: Map<string, QtMessageItem> = new Map()

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

    set_config(config: any): void {
        this.show_keys = config.show_keys || []
        this.re_filter()
    }

    re_filter(): void {
        this.el.innerHTML = ""
        this.childs = []
        this.displayed_items.clear()

        let messagesArray = Array.from(this.all_messages.values()).reverse()
        for (let msg of messagesArray) {
            if (this.show_keys.includes(msg.key)) {
                this.add_displayed_item(msg)
            }
        }
    }

    add_displayed_item(msg: any): void {
        let item = new QtMessageItem().set_msg(msg)
        this.displayed_items.set(msg.key, item)
        this.add_child(item)
    }

    add_message(msg: any): void {
        this.all_messages.set(msg.key, msg)

        if (!this.show_keys.includes(msg.key)) {
            return
        }

        let existingItem = this.displayed_items.get(msg.key)

        if (existingItem) {
            existingItem.set_msg(msg)
        } else {
            let item = new QtMessageItem().set_msg(msg)
            this.displayed_items.set(msg.key, item)

            if (this.childs.length > 0) {
                this.el.insertBefore(item.el, this.childs[0].el)
                this.childs.unshift(item)
            } else {
                this.add_child(item)
            }
        }
    }
}

export default QtMessageList