import { GNode } from "../gnode";
import web_dom from "../../../web/web_dom"
import { Line, line } from "../line";
import { Rect, rect } from "../rect";
import { Circle, circle } from "../circle";
import { Text, text } from "../text";
import { Node } from "../../../web/cls";
import { Svg, svg } from "../svg";
import { div, Div } from "../../dom/div";
import Constant from "../../../web/constant";
import { button } from "../../dom/button";
import { Input, input } from "../../dom/input";

class ProgrePoint extends GNode {
    rect: Rect
    text: Text
    value: number = 0
    width: number = 0
    init_node(): void {
        this.rect = this.add_child(rect())
        this.text = this.add_child(text())
    }
    set_value(value: number, x: number) {
        this.value = value
        this.text.set_html(value + "")
    }
}

export class Progress extends Div {
    main_line: Line
    min_g: GNode
    // points: ProgrePoint[]
    progre_points: GNode
    // bg: Rect
    input_line: Input
    max_value: ProgrePoint
    value: ProgrePoint
    margin: number = 10
    height: number = 0
    width: number = 0
    init_node(): void {
        // this.points = []
        this.min_g = new GNode()
        // this.bg = this.min_g.add_child(new Rect())
        this.main_line = this.min_g.add_child(new Line())
        this.value = this.min_g.add_child(new ProgrePoint())
        this.max_value = this.min_g.add_child(new ProgrePoint())
        // this.progre_points = this.add_child(new GNode())
        this.input_line = input().set_width(Constant.INPUT_NUMBER_WIDTH)
        this.add_childs([
            svg().add_childs([this.min_g]).set_width(1),
            button().set_html("<<").click(() => this.set_value(this.value.value + 1)),
            this.input_line,
            button().set_html("go").click(() => this.set_value(this.input_line.get_int())),
            button().set_html(">>").click(() => this.set_value(this.value.value - 1)),
        ]).set_direction(Constant.VERTICAL)
        web_dom.bind_key((tp: string, e: KeyboardEvent) => {
            console.log(tp, e.key, e.code)
            if (tp == 'keydown' && e.key == '>') {

            }
        })
    }
    on_change(value: number) {

    }
    set_max_value(value: number) {
        this.max_value.set_value(value, this.width)
        this.on_change(this.value.value)
        return this
    }
    set_value(value: number, pos?: number) {
        if (value < 0 || value > this.max_value.value) {
            value = this.value.value
        }
        if (pos == null) {
            pos = value / this.max_value.value * this.width
        }
        this.input_line.set_value(value)
        this.value.set_value(value, pos)
        this.on_change(value)
        return this
    }
    init_event() {
        web_dom.bind_drag(this.el, (state: string, x: number, y: number) => {
            if (state == 'start') {
                //this.cur_point.set_color(Constant.COLOR_YELLOW)
                this.value.x = this.value.get_x()
                this.value.y = this.value.get_y()
            }
            else if (state == 'move') {
                let pos = Math.min(this.value.x + x, this.width)
                this.set_value(Math.floor(pos / this.width), pos)
            } else {
                // this.cur_point.set_color(Constant.COLOR_BALCK)
            }
        })

    }
    draw() {
        let rect = this.parent.get_rect()
        this.height = rect.height / 2
        this.width = rect.width - 2 * this.margin
        // this.bg.set_wh(rect.width, rect.height)
        this.main_line.set_d([
            { x: this.margin, y: this.height },
            { x: this.width + this.margin, y: this.height }
        ])
        this.set_option(new Node())
    }
    on_mount(): void {
        this.draw()
    }
    set_option(option: Node): this {
        this.set_max_value(option.data || 100)
        this.set_value(option.value || 0)
        return this
    }

}
export function progress_dev() {
    return new Progress()
}
export function progress() {
    return new Progress()

}