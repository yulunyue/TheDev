import web_dom from "../../web/web_dom"
import { Node, Dom, Style } from "../../web/cls"
import util from "../../tool/util"
import { Div } from "../dom/div"
export class GNode extends Div {
    el: any
    parent: any
    children: any[]
    x: number
    y: number
    option: Node
    _on_change: any
    constructor(name: string = "g") {
        super(name)
        this.el = this.create_element(name)
        this.parent = null
        this.children = []
        this.x = 0
        this.y = 0
        this.option = new Node()
        this.init_node()
        this.init_style()
        this.init_event()

    }
    fill(color: string) {
        this.set_style({ fill: color })
    }
    on_change(call_back: any) {
        this._on_change = call_back
        return this
    }
    init_event() {

    }
    init_style() {

    }
    init_node() {

    }
    set_font_size(value: number) {
        return this.set_style({ fontSize: value })
    }
    create_element(name: string) {
        return web_dom.createElementNS(name)
    }
    set_pos(y: number, x: number): this {
        return this.set_x(x).set_y(y)
    }
    set_width(w: number): this {
        this.set_attr("width", w)
        return this
    }
    set_height(w: number): this {
        this.set_attr("height", w)
        return this
    }
    update_pos() {
        return this.set_style({ transform: `translate(${Math.floor(this.x)}px, ${Math.floor(this.y)}px)` })
    }
    set_attr(key: string, value: any): this {
        if (value == undefined || value == null) {
            return this
        }
        this.el.setAttribute(key, value)
        return this
    }
    set_attrs(attrs: any) {
        for (var key in attrs) {
            this.set_attr(key, attrs[key])
        }
        return this
    }
    set_color(color: string) {
        if (color == null || color == undefined) {
            return this
        }
        return this.set_style({ fill: color, stroke: color })
    }
    set_html(s: string) {
        this.el.innerHTML = s
        return this
    }
    set_x(x: number) {
        this.x = x
        return this.update_pos()
    }
    set_y(y: number) {
        this.y = y
        return this.update_pos()
    }
    get_x() {
        return this.x
    }
    get_y() {
        return this.y
    }
}