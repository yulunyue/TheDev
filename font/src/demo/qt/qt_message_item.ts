import { Div } from "../../base/components/export"

const COLOR_MAP: any = {
    "running": { backgroundColor: "#3498db", color: "#fff" },
    "completed": { backgroundColor: "#27ae60", color: "#fff" },
    "failed": { backgroundColor: "#c0392b", color: "#fff" },
    "blocked": { backgroundColor: "#e67e22", color: "#fff" },
}

export class QtMessageItem extends Div {
    init_style(): void {
        this.set_style({
            padding: 8,
            marginBottom: 4,
            borderRadius: 4,
            fontSize: 12,
        })
    }

    render_option(): this {
        console.log(this.option)
        let key = this.option.key
        let displayMsg = `${key} ${this.option.title} ${this.option.data.status}`
        this.set_html(displayMsg)
        let style = COLOR_MAP[this.option.data.status] || {
            backgroundColor: "#2c3e50", color: "#ecf0f1"
        }
        this.set_style(style)
        return this
    }
}

export default QtMessageItem