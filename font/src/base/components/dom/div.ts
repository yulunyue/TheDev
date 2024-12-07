import web_dom from "../../web/web_dom"
import { Style, Node, Fn1, to_node, not_null } from "../../web/cls"
import { Dom } from "../../web/cls"
import Util from "../../tool/util"
import Constant from "../../web/constant"
export class DivFactory {
    static fac_map = {}
    static instance = {}
    static set(key: string, value: any) {
        DivFactory.instance[key] = value
    }
    static get(key: string) {
        if (!DivFactory.instance[key]) {
            console.log(DivFactory.instance)
        }
        return DivFactory.instance[key]
    }
    static register(key: string, fun: any) {
        DivFactory.fac_map[key] = fun
    }
    static new_div(key: string, option: Node) {
        // console.log(key, DivFactory.fac_map)
        return this.fac_map[key]().set_option(option)
    }
}
export class Div {
    el: HTMLElement
    div_el: HTMLElement
    node_type: string
    childs: Div[]
    parent: Div
    option: Node
    index: number
    on_mount_call: any
    direction: number = -1
    layout_type: number = 0
    size: number = 0
    on_change: any = null
    change(call: any) {
        this.on_change = call
        return this
    }
    set_class(name: string) {
        return this.set_attr("class", name)
    }
    set_color(s: string) {
        this.set_style({
            color: s
        })
    }
    do_change() {
        this.on_change?.()
        return this
    }
    set_direction(direction: number) {
        if (direction != 0 && direction != -1 && direction != 1) {
            return this
        }
        this.direction = direction
        return this
    }
    get_content_divs() {
        let ret = []
        return ret
    }
    get_direction(direction: number) {
        if (this.direction != -1) {
            return this.direction
        }
        return direction
    }
    get_child(idx: number, call: any) {
        if (this.childs[idx]) {
            return this.childs[idx]
        }
        this.childs[idx] = this.add_child(call())
        return this.childs[idx]
    }
    flex_horizontal_layout() {
        this.set_size(1)
        return this.set_flex_style(
            Constant.HORIZONTAL
        ).full()
    }
    full() {
        return this.set_style({
            width: 1,
            height: 1
        })
    }
    flex_veritcal_layout() {
        this.set_size(1)
        return this.set_flex_style(Constant.VERTICAL).full()
    }

    set_abs_style(option: Node, direction: number) {
        this.clear().full()
        function dfs(node: Div, option: Node, direction: number) {
            node.set_border()
            let lt = 0
            for (var i = 0; i < option.childs.length; i++) {
                let tmp = DivFactory.new_div(option.childs[i].type, option.childs[i])
                let style: Style = {
                    left: 0,
                    top: 0,
                    width: 1,
                    height: 1,
                }
                if (direction == Constant.VERTICAL) {
                    style.left = lt / option.size_calc
                    style.width = option.childs[i].size_calc / option.size_calc
                } else {
                    style.top = lt / option.size_calc
                    style.height = option.childs[i].size_calc / option.size_calc
                }
                lt += option.childs[i].size_calc
                tmp.set_style(style)
                dfs(tmp, option.childs[i], 1 - direction)
                node.add_child(tmp)
            }
        }
        dfs(this, to_node(option).calc_size(), direction)
        return this

    }
    set_style_flex(direction: number) {
        return this.set_div_style({
            flexDirection: direction == Constant.VERTICAL ? "row" : "column",
            display: "flex",
            justifyContent: "center",
            alignContent: "center",
            flexGrow: this.size + "",

        })
    }
    set_border() {
        return this.set_div_style({ border: "1px solid #ccc" })
    }
    set_style_flex2(direction: number) {
        this.set_style_flex(direction)
        this.set_border()
        return this
    }
    set_flex_style(direction: number) {
        direction = this.get_direction(direction)
        this.set_style_flex2(direction)
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
        this.div_el = this.el
        this.option = new Node()
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
    set_style_ab_full() {
        return this.set_div_style({
            position: "fixed",
            width: 1,
            height: 1
        })
    }
    show() {
        return this.set_div_style({ display: "" })
    }
    hide() {
        return this.set_div_style({ display: "none" })
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
    set_style_ab_center() {
        return this.set_style({
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%,-50%)"
        })
    }
    init_style() {

    }
    init_event() {

    }
    set_center() {
        this.set_style({ textAlign: "center" })
    }
    create_element(name: string): any {
        return web_dom.createElement(name)
    }
    init_node() {

    }
    mount(el: Dom) {
        el.appendChild(this.div_el)
        return this
    }
    emit_mount() {
        for (var key in this.on_mount_call) {
            this[key].apply(this, this.on_mount_call[key])
        }
        for (var i = 0; i < this.childs.length; i++) {
            this.childs[i].emit_mount()
        }
        this.on_render()
        this.on_mount()
        return this
    }
    on_render() {

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
        c.set_parent(this)
        c.index = this.childs.length
        this.childs.push(c)
        return c
    }
    set_parent(p: any) {
        this.parent = p
        return this
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
    select(v: any) {
        return this
    }
    set_option(option: Node) {
        this.option.set_option(option)
        this.set_direction(option.direction)
        DivFactory.set(this.option.key, this)
        this.render_option()
        return this
    }
    update_option(option: Node, cls: any) {
        this.set_option(option)

        for (var i = 0; i < this.childs.length; i++) {
            if (option.childs[i]) {
                this.childs[i].set_option(option.childs[i])
            }
        }
        console.log(this.childs.length, option.childs.length)
        for (var i = this.childs.length; i < option.childs.length; i++) {
            this.add_child(new cls()).set_option(option.childs[i])
        }
        let childs_l = this.childs.length;
        for (var i = option.childs.length; i < childs_l; i++) {
            // console.log(i)
            // let n = this.childs.splice(i, 1)
            // this.el.removeChild(n[0].el)
        }
    }
    remove(i: number) {

    }
    render_option() {
        this.set_html(this.option.title)
    }
    add_childs(childs: any[]) {
        return this.set_childs(childs)
    }
    set_html(text: string | Fn1<any, string>) {
        if (text == null || text == undefined) {
            return this
        }
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
