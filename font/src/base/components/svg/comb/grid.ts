import { GNode } from "../gnode";
import { Line } from "../line";
import { Text } from "./div_text";
import { SvgNode } from "../svg";
import { Circle } from "../circle";
import { Rect, Polygon } from "../rect";
import web_dom from "../../../web/web_dom";
import { Constant } from "../../export";
import { Dom } from "../../../web/cls";
const NODE_GEN = {

}
export class Grid extends SvgNode {
    g: GNode
    bg: Rect
    top: number
    left: number
    cell_width: number
    cell_height: number
    init_event(): void {
        web_dom.bind_mousemove(this.el, (e: any) => {
            let x = Math.floor((e.offsetX - this.left) / this.cell_width)
            let y = Math.floor((e.offsetY - this.top) / this.cell_height)
            if (x < 0 || y < 0 || x >= this.option.data.x || y >= this.option.data.y) {
                return
            }
            this.event_hander[Constant.EVENT_MOVE]?.(e.offsetY, e.offsetX, y, x)
        })
    }
    init_node(): void {
        this.g = new GNode()
        this.bg = new Rect()
        this.add_childs([
            this.bg,
            this.g
        ])
    }
    draw_background() {
        this.bg.set_color(Constant.COLOR_WHITE1).set_wh(
            this.option.data.width,
            this.option.data.height
        )
    }
    draw_child() {
        // for (var i = 0; i < this.option.childs.length; i += 1) {
        //     let op = this.option.childs[i]
        //     let fun = NODE_GEN[op.type] || Text
        //     let el: Text = new fun().set_option(op)
        //     el.set_width(this.cell_width).set_height(this.cell_height)
        //     el.set_x(op.x * this.cell_width).set_y(op.y * this.cell_height)
        //     this.g.add_child(el)
        // }
    }
    init_data() {
        let rect = this.get_rect()
        this.option.data.width = this.option.data.width || rect.width
        this.option.data.height = this.option.data.height || rect.height
        this.cell_width = this.option.data.height / (this.option.data.y + 1)
        this.cell_height = this.option.data.width / (this.option.data.x + 1)
        this.top = this.cell_height / 2
        this.left = this.cell_width / 2
        console.log(this.option.data)

    }
    draw_lines() {

        for (var i = 0; i <= this.option.data.y; i++) {
            let datas = [
                { x: this.left, y: i * this.cell_height + this.top },
                { x: this.option.data.width - this.left, y: i * this.cell_height + this.top }
            ]
            let l = new Line().set_d(datas)

            this.g.add_child(l)
        }
        for (var i = 0; i <= this.option.data.x; i++) {
            let datas = [
                { x: i * this.cell_width + this.left, y: this.top },
                { x: i * this.cell_width + this.left, y: this.option.data.height - this.top }
            ]
            this.g.add_child(new Line().set_d(datas))
        }
    }
    draw() {
        this.init_data()
        this.g.clear()
        this.draw_background()
        this.draw_lines()
        // this.draw_child()
    }

    render_option(): void {
        web_dom.next_frame(() => this.draw())
    }

}