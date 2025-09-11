import { GNode } from "../gnode";
import { Line } from "../line";
import { Text } from "./div_text";
import { SvgNode } from "../svg";
import { Circle } from "../circle";
import { Rect, Polygon } from "../rect";
const NODE_GEN = {

}
export class Grid extends SvgNode {
    g: GNode
    width = 400
    height = 400
    h = 10
    w = 10
    cell_width: number
    cell_height: number
    init_node(): void {
        this.g = this.add_child(new GNode())
    }
    draw_child() {

        for (var i = 0; i < this.option.childs.length; i += 1) {
            let op = this.option.childs[i]
            let fun = NODE_GEN[op.type] || Text
            let el: Text = new fun().set_option(op)
            el.set_width(this.cell_width).set_height(this.cell_height)
            el.set_x(op.x * this.cell_width).set_y(op.y * this.cell_height)
            this.g.add_child(el)
        }
    }
    init_data() {
        if (this.option.x) {
            this.width = this.option.x
        }
        if (this.option.y) {
            this.height = this.option.y
        }
        if (this.option.data.h) {
            this.h = this.option.data.h
        }
        if (this.option.data.w) {
            this.w = this.option.data.w
        }
        this.cell_width = this.height / this.h
        this.cell_height = this.width / this.w
        this.set_style({
            width: this.width,
            height: this.height
        })
    }
    draw_bg_line() {
        for (var i = 0; i <= this.h; i++) {
            let datas = [
                { x: 0, y: i * this.cell_height },
                { x: this.w * this.cell_width, y: i * this.cell_height }
            ]
            console.log(datas)
            this.g.add_child(new Line().set_d(datas))
        }
        for (var i = 0; i <= this.w; i++) {
            let datas = [
                { x: i * this.cell_width, y: 0 },
                { x: i * this.cell_width, y: this.h * this.cell_height }
            ]
            this.g.add_child(new Line().set_d(datas))
        }
    }
    draw() {
        this.init_data()
        this.g.clear()
        this.draw_bg_line()
        // this.draw_child()
    }

    render_option(): void {
        this.draw()
    }

}
export function grid() {
    return new Grid()
}