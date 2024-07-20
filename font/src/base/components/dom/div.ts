import web_dom from "../../web/web_dom"
import { Style } from "src/base/web/cls"
import { Dom } from "../../web/cls"
export class Div {
    el: Dom
    div_el: Dom
    node_type: string
    childs: Div[]
    parent: Div
    on_mount_call: any
    constructor(node_type: string = 'div', parent_node_type: string = "div") {
        this.childs = []
        this.on_mount_call = {}
        this.node_type = node_type || 'div'
        this.el = this.create_element(this.node_type)
        this.parent = null
        if (parent_node_type) {
            this.div_el = web_dom.createElement(parent_node_type)
            this.div_el.appendChild(this.el)
            this.init_default_div_style()
        } else {
            this.div_el = this.el
        }
        this.init_node()
        this.init_style()
        this.init_event()
    }
    get_value(): any {
        return this.el.innerHTML
    }
    x(v: number) {
        if (0 <= v && v <= 1) {
            return this.parent.get_width() * v
        }
        return v
    }
    get_x() {
        return this.el.clientLeft
    }
    get_y() {
        return this.el.clientTop
    }
    y(v: number) {
        if (0 <= v && v <= 1) {
            return this.parent.get_height() * v
        }
        return v
    }
    get_width() {
        return this.el.clientWidth
    }
    get_height() {
        return this.el.clientHeight
    }
    render() {

    }
    init_default_div_style() {
        this.set_div_style({
            width: 1,
            height: 1,
            position: "absolute"
        })
    }
    set_attr(key: string, value: any) {
        this.el.setAttribute?.(key, value)
        return this
    }
    get_attr(key: string) {
        return this.el.getAttribute(key)
    }
    set_size(w: number, h: number) {
        this.set_div_style({ width: w, height: h })
        return this
    }
    set_pos(x: number, y: number) {
        return this
    }
    set_div_style(style: Style) {
        web_dom.set_el_style(this.div_el, style)
        return this
    }
    set_style(style: Style) {
        web_dom.set_el_style(this.el, style)
        return this
    }
    init_style() {

    }
    init_event() {

    }
    create_element(name: string): HTMLElement | SVGElement {
        return web_dom.createElement(name)
    }
    init_node() {

    }
    mount(el: HTMLElement) {
        el.appendChild(this.div_el)
        this.render()
        return this
    }
    on_mount() {
        for (var key in this.on_mount_call) {
            this[key].apply(this, this.on_mount_call[key])
        }
        for (var i = 0; i < this.childs.length; i++) {
            this.childs[i].on_mount()
        }
        return this
    }
    add_child(c: any) {
        c.mount(this.el)
        c.parent = this
        this.childs.push(c)
        return this
    }
    set_childs(childs: Div[]) {
        for (var i = 0; i < childs.length; i++) {
            this.add_child(childs[i])
        }
        return this
    }
    add_childs(childs: Div[]) {
        return this.set_childs(childs)
    }
    set_html(text: string) {
        this.el.innerHTML = text
        return this
    }
    set_value(value: any) {
        (this.el as any).value = value
        return this
    }

}

export function div(node_type?: string) {
    return new Div(node_type)
}
