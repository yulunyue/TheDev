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
    start_x: number
    start_y: number
    init_node(): void {
        this.rect = this.add_child(rect())
        this.rect.set_wh(7, 14).set_color(Constant.COLOR_BALCK).set_y(-10)
        this.text = this.add_child(text())
        this.text.set_y(14).set_x(2)
    }
    set_value(value: number, x: number) {
        this.value = value
        this.text.set_html(value + "")
        this.set_x(x)
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
    _on_change:any
    margin: number = 10
    height: number = 0
    width: number = 0
    init_node(): void {
        // this.points = []
        this.min_g = new GNode()
        // this.bg = this.min_g.add_child(new Rect())
        this.main_line = this.min_g.add_child(new Line().with_arrow())
        this.value = this.min_g.add_child(new ProgrePoint())
        this.max_value = this.min_g.add_child(new ProgrePoint())
        // this.progre_points = this.add_child(new GNode())
        this.input_line = input().set_width(Constant.INPUT_NUMBER_WIDTH)
        this.add_childs([
            svg().add_childs([this.min_g]).set_width(1),
            button().set_html("<<").click(() => this.set_value(this.value.value - 1)),
            this.input_line,
            button().set_html("go").click(() => this.set_value(this.input_line.get_int())),
            button().set_html(">>").click(() => this.set_value(this.value.value + 1)),
        ]).set_direction(Constant.VERTICAL)
        web_dom.bind_key((tp: string, e: KeyboardEvent) => {
            if (tp == 'keydown' && e.key == Constant.KEY_RIGHT) {
                this.set_value(this.value.value + 1)
            }
            else if (tp == 'keydown' && e.key == Constant.KEY_LEFT) {
                this.set_value(this.value.value - 1)
            }
        })
    }
    change(callback:any){
        this._on_change=callback
        return this
    }
    on_change(value: number) {
        this._on_change?.(value)
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
        this.value.set_value(value, pos + this.margin)
        this.on_change(value)
        return this
    }
    init_event() {
        web_dom.bind_drag(this.el, (state: string, x: number, y: number) => {
            if (state == 'start') {
                //this.cur_point.set_color(Constant.COLOR_YELLOW)
                this.value.start_x = this.value.get_x()
                this.value.start_y = this.value.get_y()

            }
            else if (state == 'move') {
                let pos = Math.min(this.value.start_x + x, this.width)
                this.set_value(Math.floor(pos * this.max_value.value / this.width), pos)
            } else {
                // this.cur_point.set_color(Constant.COLOR_BALCK)
            }
        })

    }
    draw() {
        let rect = this.min_g.parent.get_rect()
        this.height = rect.height / 2
        this.value.set_y(this.height)
        this.max_value.set_y(this.height)
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
        this.set_max_value(option.childs.length)
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