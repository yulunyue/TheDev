import web_dom from "../../web/web_dom"
import { Node, Dom } from "../../web/cls"

export class GNode {
    el: Dom
    on_mount_call: any
    parent: any
    childs: GNode[]
    constructor(name: string = "g") {
        this.el = this.create_element(name)
        this.parent = null
        this.childs = []
        this.on_mount_call = {}
        this.init_style()
        this.init_node()
        this.init_event()
    }
    init_event() {

    }
    init_style() {

    }
    init_node() {

    }
    create_element(name: string) {
        return web_dom.createElementNS(name)
    }
    set_pos(x: number, y: number): this {
        return this.set_x(x).set_y(y)
    }
    get_attr(key: string) {
        return this.el.getAttribute(key)
    }
    set_style(s: any) {
        for (var k in s) {
            this.el.style[k] = s[k]
        }
        return this
    }
    mount(el: any) {
        el.appendChild(this.el)
    }
    add_child(c: any) {
        c.mount(this.el)
        c.parent = this
        c.index = this.childs.length
        this.childs.push(c)
        return c
    }
    clear() {
        this.set_html("")
    }
    set_attr(key: string, value: any) {
        this.el.setAttribute(key, value)
        return this
    }
    set_color(color: string) {
        return this.set_style({ fill: color })
    }
    x(v: any) {
        return v
    }
    y(v: any) {
        return v
    }
    set_html(s: string) {
        this.el.innerHTML = s
        return this
    }
    set_x(x: number) {
        return this.set_attr("x", x)
    }
    set_y(y: number) {
        return this.set_attr("y", y)
    }
    get_x() {
        return parseFloat(this.get_attr("x"))
    }
    get_y() {
        return parseFloat(this.get_attr("y"))
    }
    set_option(option: Node): this {
        return this.set_x(
            option.data.x
        ).set_y(
            option.data.y
        )
    }
    on_mount() {

    }
    emit_mount() {
        this.on_mount()
    }

}
export function gnode(name: string = "g") {
    return new GNode(name)
}