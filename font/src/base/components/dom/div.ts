import web_dom from "../../web/web_dom"
import { Style } from "src/base/web/cls"
export class Div {
    el: HTMLElement
    div_el: HTMLElement
    constructor() {
        this.div_el = web_dom.createElement("div")
        this.init_node()
        this.init_style()
        this.init_event()
        this.div_el.appendChild(this.el)
        this.init()
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
    static create_element(name: string) {
        return web_dom.createElement(name)
    }
    init_node() {
        this.el = Div.create_element("div")
    }
    init() {

    }
    mount(el: HTMLElement) {
        el.appendChild(this.div_el)
        return this
    }
    add_child(c: Div) {
        c.mount(this.el)
    }
    set_childs(childs: Div[]) {
        for (var i = 0; i < childs.length; i++) {
            this.add_child(childs[i])
        }
        return this
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

export function div() {
    return new Div()
}