import { GNode } from "../gnode";
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

export class Progress extends Svg {
    direction: 'VERTICAL' | 'HORIZONTAL'
    main_line: Line
    cur_point: Circle
    points: ProgrePoint[]
    progre_points: GNode
    init_node(): void {
        this.direction = 'VERTICAL'
        this.points = []
        this.cur_point = new Circle()
        this.main_line = new Line()
        this.progre_points = new GNode()
        this.add_childs([this.cur_point, this.main_line, this.progre_points])

    }
    on_mount(): void {
        console.log(this.el, this.get_rect())
    }
    set_option(option: Node): this {
        return this
    }

}
export function progress_dev() {
    return new Progress()
}