import { Div, web_dom, Row } from "../base/components/export"

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
        this.el.addEventListener("mousedown", (e: MouseEvent) => {
            e.preventDefault()
            let startX = e.screenX
            let startY = e.screenY
            let windowX = window.screenX
            let windowY = window.screenY
            let onMove = (ev: MouseEvent) => {
                let dx = ev.screenX - startX
                let dy = ev.screenY - startY
                window.moveTo(windowX + dx, windowY + dy)
            }
            let onUp = () => {
                window.removeEventListener("mousemove", onMove)
                window.removeEventListener("mouseup", onUp)
            }
            window.addEventListener("mousemove", onMove)
            window.addEventListener("mouseup", onUp)
        })
    }
    render(): void {
        this.set_html("拖动窗口")
    }
}

export class QtMain extends Div {
    init_style(): void {
        this.set_style({
            width: 1,
            height: 1,
            display: "flex",
            flexDirection: "column",
        })
    }
    render(): void {
        this.add_child(new QtDragBar())
        this.add_child(new Div().set_style({
            flex: 1,
            backgroundColor: "#34495e",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#fff",
        }).set_html("Qt Browser Control"))
    }
}

export default function () {
    return new QtMain()
}