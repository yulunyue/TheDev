import web_dom from "../../web/web_dom"
import { Style } from "src/base/web/cls"
export class Div {
    el: HTMLElement | SVGElement
    div_el: HTMLElement | SVGElement
    node_type: string
    constructor(node_type: string, parent_node_type: string = "div") {
        this.node_type = node_type
        this.el = this.create_element(this.node_type)
        if (parent_node_type) {
            this.div_el = this.create_element(parent_node_type)
            this.div_el.appendChild(this.el)
        } else {
            this.div_el = this.el
        }
        this.init_node()
        this.init_style()
        this.init_event()
        this.init()
    }
    set_attr(key: string, value: any) {
        this.el.setAttribute?.(key, value)
        return this
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
    init() {

    }
    mount(el: HTMLElement) {
        el.appendChild(this.div_el)
        return this
    }
    add_child(c: any) {
        c.mount(this.el)
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