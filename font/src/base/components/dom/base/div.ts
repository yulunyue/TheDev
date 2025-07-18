import web_dom from "../../../web/web_dom"
import { Style, Node, Fn1, to_node, not_null, node } from "../../../web/cls"
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
    do_change(src?: any, dst?: any) {
        this.event_hander[Constant.EVENT_CHANGE]?.(src, dst)
        return this
    }
    on_change(call: any) {
        this.event_hander[Constant.EVENT_CHANGE] = call
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
            color: s
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
            position: "absolute"
        })
    }

    set_flex_grow(grow: number) {
        return this.set_div_style({
            flexGrow: grow + ""
        })
    }
    set_border() {
        return this.set_div_style({ border: "1px solid #ccc" })
    }
    constructor(node_type: string = 'div', parent_node_type: string = "div") {
        this.childs = []
        this.event_hander = {}
        this.node_type = node_type || 'div'
        this.el = this.create_element(this.node_type)
        this.parent = null
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
    set_style_flex(direction: number) {
        return this.set_div_style({
            flexDirection: direction == Constant.VERTICAL ? "row" : "column",
            display: "flex",
            justifyContent: "center",
            alignContent: "center",
            flexGrow: this.size + "",
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
    set_childs(childs: Node[], cls: any) {
        for (var i = 0; i < childs.length; i++) {
            let c = this.childs[i]
            if (c) {
                c.set_option(childs[i])
            } else {
                this.add_child(cls().set_option(childs[i]))
            }
        }
        for (var i = childs.length; i < this.childs.length; i++) {
            this.childs[i].hide()
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
        if (this.option.title) {
            this.set_title(this.option.title)
        }
        if (this.option.id) {
            DivFactory.set(this.option.id, this)
        }
        this.render_option()
        return this
    }
    update_option(option: Node, cls: any) {
        // this.set_childs(option.childs,cls)
        // this.set_option(option)
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
        console.log(this.option.id,this.option.local_storge_enable,value)
        if (this.option.id && this.option.local_storge_enable) {
            web_dom.set_local(this.option.id, value.dump())
        }
        this.do_select(value)
        return this
    }


}