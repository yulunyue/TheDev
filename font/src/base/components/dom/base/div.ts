import web_dom from "../../../web/web_dom"
import { Style, Node, Fn1, Fn3Void, to_node, not_null, node } from "../../../web/cls"
import { Dom } from "../../../web/cls"
import Util from "../../../tool/util"
import Constant from "../../../web/constant"
import { DivFactory } from "./div_factory"
export class Div {
    el: HTMLElement
    node_type: string
    childs: Div[]
    parent: Div
    option: Node
    index: number
    size: number = 0
    _value: any = null
    event_hander: any
    disable(state: boolean) {
        if (state) {
            this.set_attr("disabled", "disabled")
        } else {
            this.set_attr("disabled", "enabled")
        }
        return this
    }
    init_table_style(): void {

    }
    do_change(key: string, src?: any, dst?: any) {
        if (src == null && dst == null) {
            return this
        }
        this.event_hander[Constant.EVENT_CHANGE]?.(key, src, dst)
        return this
    }
    on_change(call: Fn3Void<string, Node, Node>) {
        this.event_hander[Constant.EVENT_CHANGE] = call
        return this
    }
    on_move(call: any) {
        this.event_hander[Constant.EVENT_MOVE] = call
        return this
    }
    on_click(call_back: any) {
        web_dom.bind_click(this.el, call_back)
        return this
    }
    do_select(arg: any) {
        this.event_hander[Constant.EVENT_CHANGE]?.(this._value, arg)
        this._value = arg
        return this
    }
    on_select(call: any) {
        this.event_hander[Constant.EVENT_CHANGE] = call
        return this
    }
    set_class(name: string) {
        return this.set_attr("class", name)
    }
    set_color(s: string) {
        this.set_style({
            backgroundColor: s
        })

    }
    get_child(idx: number, call: any) {
        if (this.childs[idx]) {
            return this.childs[idx]
        }
        this.childs[idx] = this.add_child(call())
        return this.childs[idx]
    }
    full() {
        return this.set_style({
            width: 1,
            height: 1,
            // position: "absolute"
        })
    }

    set_border() {
        return this.set_div_style({ border: "1px solid #ccc" })
    }
    constructor(node_type: string = 'div') {
        this.childs = []
        this.event_hander = {}
        this.node_type = node_type || 'div'
        this.el = this.create_element(this.node_type)
        this.parent = null
        this.option = new Node()
        this.do_change = this.do_change.bind(this)
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
    set_flex_style_column() {
        this.set_style({
            display: "flex",
            flexDirection: "row",
            alignItems: "center"
        })
    }
    show() {
        return this.set_style({ display: "" })
    }
    hide() {
        return this.set_style({ display: "none" })
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
            top: this.get_y(),
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
        return this._value
    }
    get_abs_x() {
        return this.el.offsetLeft
    }
    get_abs_y() {
        return this.el.offsetTop
    }
    get_x() {
        return this.el.clientLeft
    }
    get_y() {
        return this.el.clientTop
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
        // 尽可能的压缩
        this.size = size
        this.set_style({ flex: size + "" })
        return this
    }
    scroll_to_bottom() {
        this.el.scrollTo(0, this.el.scrollHeight)
    }
    set_flex(size: number) {
        // 尽量不压缩
        this.size = size
        this.set_style({ flexGrow: size + "" })
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
        web_dom.set_el_style(this.el, style)
        return this
    }
    set_style(style: Style) {
        web_dom.set_el_style(this.el, style)
        return this
    }
    set_style_center_by_position() {
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
    set_style_text_center() {
        this.set_style({ textAlign: "center" })
    }
    create_element(name: string): any {
        return web_dom.createElement(name)
    }
    init_node() {

    }
    mount(el: Dom) {
        el.appendChild(this.el)
        this.on_mount()
        return this
    }
    emit_mount() {
        for (var i = 0; i < this.childs.length; i++) {
            this.childs[i].emit_mount()
        }
        this.on_render()
        return this
    }
    on_render() {

    }
    on_mount() {

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
    parse_child_option(o: Node) {  //原地修改子类的option

    }
    set_childs(childs: any, cls: any) {
        let idx = 0
        while (idx < childs.length) {
            this.parse_child_option(childs[idx])
            if (this.childs[idx]) {
                this.childs[idx].set_option(childs[idx]).show()
            } else {
                this.add_child(cls(childs[idx]))
            }
            idx += 1
        }
        while (idx < this.childs.length) {
            this.childs[idx].hide()
            idx += 1
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
    set_title(s: string) {
        return this
    }
    set_option(option: Node) {
        this.option.set_option(option)
        this.render_option()
        if (this.option.title) {
            this.set_title(this.option.title)
        }
        if (this.option.size) {
            this.set_size(this.option.size)
        }
        if (this.option.color) {
            this.set_color(this.option.color)
        }
        if (this.option.id) {
            DivFactory.set(this.option.id, this)
        }
        return this
    }

    remove(i: number) {

    }
    render_option() {

    }
    add_childs(childs: any[]) {
        for (var i = 0; i < childs.length; i++) {
            this.add_child(childs[i])
        }
        return this
    }
    set_html(text: string | Fn1<any, string>) {
        if (typeof text == 'function') {
            text(this.el)
            return this
        }
        this.el.innerHTML = text
        return this
    }
    set_uri(s: string) {
        web_dom.post(s, (data: Node) => {
            this.set_option(data)
        })
        return this
    }
    set_value(value: any) {
        // console.trace(value)
        return this
    }

}