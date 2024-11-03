import { GNode } from "../gnode";
import web_dom from "../../../web/web_dom"
import { Line, line } from "../line";
import { Rect, rect } from "../rect";
import { Circle, circle } from "../circle";
import { Text, text } from "../text";
import { Node } from "../../../web/cls";
import { Svg } from "../svg";
class ProgrePoint extends GNode {
    rect: Rect
    text: Text

    init_node(): void {

    }
}

export class Progress extends GNode {
    main_line: Line
    cur_point: Circle
    points: ProgrePoint[]
    progre_points: GNode
    bg: Rect
    init_node(): void {
        this.points = []
        this.bg = this.add_child(new Rect())
        this.main_line = this.add_child(new Line().with_arrow())
        this.cur_point = this.add_child(new Circle())
        this.progre_points = this.add_child(new GNode())
    }
    init_event() {
        web_dom.bind_drag(this.el, (state: string, x: number, y: number) => {
            console.log(state, x, y)
        })

    }
    draw() {
        let rect = this.parent.get_rect()
        let margin = 10
        let height = rect.height / 2
        this.bg.set_wh(rect.width, rect.height).set_color("")
        this.main_line.set_d([
            { x: margin, y: height },
            { x: rect.width - margin * 2, y: height }
        ])
        this.cur_point.set_pos(margin, height).set_r(5)
    }
    on_mount(): void {
        this.draw()
    }
    set_option(option: Node): this {
        return this
    }

}
export function progress_dev() {
    return new Progress()
}
export function progress() {
    return new Progress()
}