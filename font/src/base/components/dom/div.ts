import web_dom from "../../web/web_dom"
import { Style, Node, Fn1 } from "src/base/web/cls"
import { Dom } from "../../web/cls"
import Constant from "../../web/constant"

export class Div {
    el: HTMLElement
    div_el: HTMLElement
    node_type: string
    childs: Div[]
    parent: Div
    dialog: Div
    option: Node
    index: number
    on_mount_call: any
    direction: number = null
    layout_type: number = 0
    size: number = 0
    set_direction(direction: number) {
        this.direction = direction
        return this
    }
    get_direction(direction: number) {
        if (this.direction != null) {
            return this.direction
        }
        return direction
    }
    add_grid_childs(childs: any[]) {
        let row = Math.ceil(Math.sqrt(childs.length))
        let col = Math.ceil(childs.length / row)
        for (var i = 0; i < row; i++) {
            let tmp_layout = new Div().set_size(1)
            for (var j = 0; j < col; j += 1) {
                let idx = i * col + j
                if (idx >= childs.length) {
                    break
                }
                tmp_layout.add_child(childs[idx])
            }
            this.add_child(tmp_layout)
        }
        return this
    }
    flex_horizontal_layout() {
        this.set_size(1)
        return this.set_flex_style(Constant.HORIZONTAL)

    }
    flex_veritcal_layout() {
        this.set_size(1)
        return this.set_flex_style(Constant.VERTICAL)
    }
    abs_horizontal_layout() {
        this.set_abs_style(Constant.HORIZONTAL)
    }
    abs_veritcal_layout() {
        this.set_abs_style(Constant.VERTICAL)
    }
    set_abs_style(direction: number) {
        this.set_div_style({
            width: 1,
            height: 1,
            position: "absolute"
        })
        direction = this.get_direction(direction)
        for (var i = 0; i < this.childs.length; i++) {
            this.childs[i].set_div_style({
                left: direction == Constant.VERTICAL ? i / this.childs.length : 0,
                width: direction == Constant.VERTICAL ? 1 / this.childs.length : 1,
                height: direction == Constant.HORIZONTAL ? 1 / this.childs.length : 1,
                top: direction == Constant.HORIZONTAL ? i / this.childs.length : 0,
                position: "absolute",
                border: "1px solid #000"
            })
            if (this.childs[i].set_abs_style) {
                this.childs[i].set_abs_style(1 - direction)
            }
        }
        return this

    }
    set_flex_style(direction: number) {
        direction = this.get_direction(direction)
        this.set_div_style({
            flexDirection: direction == Constant.VERTICAL ? "row" : "column",
            display: "flex",
            justifyContent: "center",
            alignContent: "center",
            flexGrow: this.size + "",
            border: "1px solid #000"
        })
        for (var i = 0; i < this.childs.length; i++) {
            if (this.childs[i].set_flex_style) {
                this.childs[i].set_flex_style(1 - direction)
            }
        }
        return this

    }
    constructor(node_type: string = 'div', parent_node_type: string = "div") {
        this.childs = []
        this.on_mount_call = {}
        this.node_type = node_type || 'div'
        this.el = this.create_element(this.node_type)
        this.parent = null
        if (parent_node_type && parent_node_type != node_type) {
            this.div_el = web_dom.createElement(parent_node_type)
            this.div_el.appendChild(this.el)

        } else {
            this.div_el = this.el
        }
        this.init_default_div_style()
        this.init_node()
        this.init_style()
        this.init_event()
    }
    dump() {
        return {
            node_type: this.node_type,
            option: this.option ? this.option.dump() : null,
            rect: this.get_rect()
        }
    }
    full() {
        return this.set_div_style({
            position: "fixed",
            width: 1,
            height: 1
        })
    }
    get_dialog() {
        if (!this.dialog) {
            this.dialog = new Div("div", "").set_div_style(
                { position: "fixed" }
            ).mount(web_dom.get_body())
        }
        return this.dialog
    }
    show() {
        return this.set_div_style({ display: "" })
    }
    hide() {
        return this.set_div_style({ display: "none" })
    }
    get_p_x() {
        return (this.el as HTMLElement).offsetLeft
    }
    get_p_y() {
        return (this.el as HTMLElement).offsetTop
    }
    get_a_x() {
        return (this.el as HTMLElement).getBoundingClientRect().x;
    }
    get_a_y() {
        return (this.el as HTMLElement).getBoundingClientRect().y
    }
    get_rect() {
        return {
            left: this.get_x(),
            right: this.get_y(),
            width: this.get_width(),
            height: this.get_height()
        }
    }
    clear() {
        this.set_html("")
        this.childs = []
        return this
    }
    get_value(): any {
        return this.el.innerHTML
    }
    click(call_back: any) {
        web_dom.bind_click(this.el, call_back)
        return this
    }
    x(v: number) {
        return v
    }
    get_x() {
        return this.el.clientLeft
    }
    get_y() {
        return this.el.clientTop
    }
    y(v: number) {
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
            // width: 1,
            // height: 1,
            // position: "absolute",
            border: "1px splid #000"
        })
    }
    set_attr(key: string, value: any) {
        this.el.setAttribute?.(key, value)
        return this
    }
    get_attr(key: string) {
        return this.el.getAttribute(key)
    }
    set_size(size: number) {
        this.size = size
        return this
    }
    set_height(h: number) {
        return this.set_div_style({ height: h })
    }
    set_width(h: number) {
        return this.set_div_style({ width: h })
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
    create_element(name: string): any {
        return web_dom.createElement(name)
    }
    init_node() {

    }
    mount(el: Dom) {
        el.appendChild(this.div_el)
        this.render()
        return this
    }
    emit_mount() {
        for (var key in this.on_mount_call) {
            this[key].apply(this, this.on_mount_call[key])
        }
        for (var i = 0; i < this.childs.length; i++) {
            this.childs[i].emit_mount()
        }
        this.on_mount()
        return this
    }
    on_mount() {

    }
    mount_html(call: any) {
        this.on_mount_call["set_html"] = [() => {
            return call(this.el)
        }]
        return this
    }
    add_child(c: any) {
        c.mount(this.el)
        c.parent = this
        c.index = this.childs.length
        this.childs.push(c)
        return c
    }
    set_childs(childs: Div[]) {
        for (var i = 0; i < childs.length; i++) {
            this.add_child(childs[i])
        }
        return this
    }
    get_tree_infos() {
        let p: Div = this
        let info = []
        while (p) {
            info.push({ index: p.index, type: this.node_type })
            p = p.parent
        }
        info.reverse()
        return info
    }
    set_option(option: Node) {
        this.option = option
        return this
    }
    add_childs(childs: any[]) {
        return this.set_childs(childs)
    }
    set_html(text: string | Fn1<any, string>) {
        if (typeof text == 'function') {
            text(this.el)
            return this
        }
        this.el.innerHTML = text
        return this
    }
    set_value(value: any) {
        (this.el as any).value = value
        return this
    }

}

export function div(node_type?: string) {
    return new Div(node_type, "")
}
