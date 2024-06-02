import web_dom from "../../web/web_dom"
export class Div {
    node_type: string = "div"
    el: HTMLElement
    constructor() {
        this.init()
    }
    init() {
        this.el = web_dom.createElement(this.node_type)
    }
    mount(el: HTMLElement) {
        el.appendChild(this.el)
        return this
    }
    set_childs(childs: Div[]) {
        for (var i = 0; i < childs.length; i++) {
            childs[i].mount(this.el)
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