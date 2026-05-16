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
    left_div: Div
    right_div: Div

    init_node(): void {
        this.left_div = new Div()
        this.add_child(this.left_div)
        this.right_div = new Div()
        this.add_child(this.right_div)
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
        })
        this.left_div.set_style({
            flex: 1,
            color: "#fff",
        })
        this.right_div.set_style({
            padding: "2px 8px",
            borderRadius: 4,
            backgroundColor: "rgba(255,255,255,0.2)",
            color: "#fff",
        })
    }

    render_option(): this {
        console.log(this.option)
        let key = this.option.key
        let title = this.option.title
        let status = this.option.data.status
        this.left_div.set_html(`${key} ${title}`)
        this.right_div.set_html(status)
        let bgStyle = COLOR_MAP[status] || {
            backgroundColor: "#2c3e50", color: "#fff"
        }
        this.set_style(bgStyle)
        return this
    }
}

export default QtMessageItem