import { Div } from "../../base/components/export"

export class QtDragBar extends Div {
    init_style(): void {
        this.set_style({
            height: 30,
            backgroundColor: "#2c3e50",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#fff",
            fontSize: 12,
            userSelect: "none",
        })
    }
    init_event(): void {

    }
    render(): void {
        this.set_html("拖动窗口")
    }
}

export default QtDragBar