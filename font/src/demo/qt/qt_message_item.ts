import { Div } from "../../base/components/export"

const COLOR_MAP: any = {
    "running": { backgroundColor: "#3498db", color: "#fff" },
    "completed": { backgroundColor: "#27ae60", color: "#fff" },
    "failed": { backgroundColor: "#c0392b", color: "#fff" },
    "blocked": { backgroundColor: "#e67e22", color: "#fff" },
    "idle": { backgroundColor: "#27ae60", color: "#fff" },
    "busy": { backgroundColor: "#3498db", color: "#fff" },
}

export class QtMessageItem extends Div {
    key_div: Div
    title_div: Div

    init_node(): void {
        this.key_div = new Div()
        this.add_child(this.key_div)
        this.title_div = new Div()
        this.add_child(this.title_div)
    }

    init_style(): void {
        this.set_style({
            padding: 8,
            marginBottom: 4,
            borderRadius: 4,
            fontSize: 12,
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            justifyContent: "space-between",
            gap: 8,
        })
        this.key_div.set_style({
            minWidth: 50,
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
            color: "#fff",
        })
        this.title_div.set_style({
            flex: "1",
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
            color: "#fff",
            textAlign: "right",
        })
    }

    render_option(): this {
        console.log(this.option)
        let key = this.option.key || ""
        let title = this.option.title || ""
        let status = this.option.data?.status || ""
        
        this.key_div.set_html(key)
        this.title_div.set_html(title)
        
        let bgStyle = COLOR_MAP[status] || {
            backgroundColor: "#2c3e50", color: "#fff"
        }
        this.set_style(bgStyle)
        return this
    }
}

export default QtMessageItem