import { GNode } from "../gnode";
import web_dom from "../../../web/web_dom"
import { Line } from "../line";
import { Rect } from "../rect";
import { Text, text } from "../text";
import { Node } from "../../../web/cls";
import { SvgNode } from "../svg";
import { Div } from "../../dom/div";
import { FlexRow } from "../../dom/base/row";
import Constant from "../../../web/constant";
import { Button } from "../../dom/form/button";
import { Input } from "../../dom/form/input";

class ProgrePoint extends GNode {
    rect: Rect
    text: Text
    value: number = 0
    start_x: number
    start_y: number
    init_node(): void {
        this.rect = this.add_child(new Rect())
        this.rect.set_wh(7, 14).set_color(Constant.COLOR_BLACK).set_y(-10)
        this.text = this.add_child(text())
        this.text.set_y(14).set_x(4)
    }
    set_value(value: number, x?: number) {
        this.value = value
        this.text.set_html(value + "")
        this.set_x(x)
        return this
    }
}

export class Progress extends FlexRow {
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
    g: SvgNode
    init_style(): void {
        this.g.set_size(1)
        this.set_height(Constant.INPUT_HEIGHT)
        super.init_style()
    }
    init_node(): void {
        this.min_g = new GNode()
        this.main_line = this.min_g.add_child(new Line().with_arrow())
        this.value = this.min_g.add_child(new ProgrePoint())
        this.max_value = this.min_g.add_child(new ProgrePoint())
        this.input_line = new Input().set_width(Constant.INPUT_NUMBER_WIDTH)
        this.g = new SvgNode().add_children([this.min_g])
        this.add_children([
            this.g,
            new Button().set_html("<<").on_click(() => this.set_value(this.value.value - 1)),
            this.input_line,
            new Button().set_html("go").on_click(() => this.set_value(this.input_line.get_int())),
            new Button().set_html(">>").on_click(() => this.set_value(this.value.value + 1)),
        ])
        web_dom.bind_key((tp: string, e: KeyboardEvent) => {
            if (tp == 'keydown' && e.key == Constant.KEY_RIGHT) {
                this.set_value(this.value.value + 1)
            }
            else if (tp == 'keydown' && e.key == Constant.KEY_LEFT) {
                this.set_value(this.value.value - 1)
            }
        })
    }
    render_option(): void {

    }
    set_max_value(value: number) {
        this.max_value.set_value(value, this.width)
        return this
    }
    get_value() {
        return this.value.value
    }
    set_value(value: number, pos?: number) {
        if (isNaN(value)) {
            return this
        }
        if (value < 0 || value > this.max_value.value) {
            value = this.value.value
        }
        if (pos == null) {
            if (this.max_value.value == 0) {
                pos = 0
            } else {
                pos = value / this.max_value.value * this.width
            }
        }
        this.input_line.set_value(value)
        this.value.set_value(value, Math.min(pos + this.margin, this.width))
        this.do_select({ value: value, pos: pos })
        return this
    }
    init_event() {
        web_dom.bind_drag(this.value.el, (state: string, x: number, y: number) => {
            if (state == 'start') {

                this.value.start_x = this.value.get_x() - this.margin
                this.value.start_y = this.value.get_y()
                // console.log(this.value.get_x())
            }
            else if (state == 'move') {
                let pos = Math.min(this.value.start_x + x, this.width)
                this.set_value(Math.floor(pos * this.max_value.value / this.width), pos)
                // console.log(this.value.get_x())
            } else {
                // this.cur_point.set_color(Constant.COLOR_BLACK)
            }
        })

    }
    draw() {
        let rect = this.g.get_rect()
        this.height = rect.height / 2
        this.value.set_y(this.height)
        this.max_value.set_y(this.height)
        this.width = rect.width - 2 * this.margin
        // console.log(this.height, this.width)
        // this.bg.set_wh(rect.width, rect.height)
        this.main_line.set_d([
            { x: this.margin, y: this.height },
            { x: this.width + this.margin, y: this.height }
        ])
        this.set_option({ value: 0, data: { max_length: 0 } })
    }
    on_mount(): void {
        web_dom.next_frame(() => this.draw())
    }
    set_option(option: Node): this {
        this.set_max_value(option.data.max_length)
        this.set_value(option.value)
        return super.set_option(option)
    }

}
export function progress_dev() {
    return new Progress()
}
export function progress() {
    return new Progress()

}