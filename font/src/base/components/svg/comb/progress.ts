import { GNode } from "../gnode";
import { Line, line } from "../line";
import { Rect, rect } from "../rect";
import { Circle, circle } from "../circle";
import { Text, text } from "../text";
import { Node } from "../../../web/cls";
class ProgrePoint extends GNode {
    rect: Rect
    text: Text

    init_node(): void {

    }
}

export class Progress extends GNode {
    direction: 'VERTICAL' | 'HORIZONTAL'
    main_line: Line
    cur_point: Circle
    points: ProgrePoint[]
    init_node(): void {
        this.direction = 'VERTICAL'
        this.points = []
        this.cur_point = new Circle()
    }
    set_option(option: Node): this {
        return this
    }

}
export function progress() {
    return new Progress()
}