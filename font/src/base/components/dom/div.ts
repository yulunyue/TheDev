import web_dom from "../../web/web_dom"
export class Div {
    el: HTMLElement
    div_el: HTMLElement
    constructor() {
        this.div_el = web_dom.createElement("div")
        this.init_node()
        this.div_el.appendChild(this.el)
        this.init()
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

export default function () {
    return new Div()
}