import web_dom from "../../../web/web_dom"
import { Style, Node, Fn1, Fn3Void, to_node, not_null, node, Dom } from "../../../web/cls"
import Util from "../../../tool/util"
import Constant from "../../../web/constant"
import { DivFactory } from "./div_factory"
import { DivStyle } from "./div_style"

export interface DivStyleMethods {
    set_style(style: Style): this
    set_div_style(style: Style): this
    set_style_ab_full(): this
    set_style_center_by_position(): this
    set_style_text_center(): void
    set_flex_style_column(): this
    set_flex_style_row(): this
    set_border(): this
    get_x(): number
    get_y(): number
    get_width(): number
    get_height(): number
    get_abs_x(): number
    get_abs_y(): number
    get_a_x(): number
    get_a_y(): number
    get_rect(): { left: number; top: number; width: number; height: number }
    set_pos(x: number, y: number): this
    set_size(size: number): this
    set_flex(size: number): this
    set_height(h: number): this
    set_width(w: number): this
    set_attr(key: string, value: any): this
    get_attr(key: string): string | null
    set_class(name: string): this
    set_color(s: string): void
    full(): this
}

export class Div {
    el: HTMLElement
    node_type: string
    children: Div[]
    children_map: any
    parent: Div | null
    option: Node
    index: number
    size: number = 0
    _value: any = null
    event_hander: { [key: string]: any }

    constructor(node_type: string = 'div') {
        this.children = []
        this.children_map = {}
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

    disable(state: boolean) {
        if (state) {
            this.set_attr("disabled", "disabled")
        } else {
            this.set_attr("disabled", "enabled")
        }
        return this
    }

    init_table_style(): void { }

    do_change(key: string, src?: any, dst?: any) {
        if (src == null && dst == null) {
            return this
        }
        this.event_hander[Constant.EVENT_CHANGE]?.(key, src, dst)
        return this
    }

    on_change(call: Fn3Void<string, any, any>) {
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

    get_child(idx: number, call: any) {
        if (this.children[idx]) {
            return this.children[idx]
        }
        this.children[idx] = this.add_child(call())
        return this.children[idx]
    }

    dump() {
        return {
            node_type: this.node_type,
            option: this.option ? this.option.dump() : null,
            rect: this.get_rect()
        }
    }

    show() {
        return this.set_style({ display: "" })
    }

    hide() {
        return this.set_style({ display: "none" })
    }

    is_visible() {
        return this.el.style.display !== "none"
    }

    clear() {
        this.set_html("")
        this.children = []
        return this
    }

    get_value(): any {
        return this._value
    }

    render() { }

    init_default_div_style() {
        this.set_div_style({
            border: "1px splid #000"
        })
    }

    scroll_to_bottom() {
        this.el.scrollTo(0, this.el.scrollHeight)
    }

    init_style() { }

    init_event() { }

    create_element(name: string): any {
        return web_dom.createElement(name)
    }

    init_node() { }

    mount(el: Dom) {
        el.appendChild(this.el)
        this.on_mount()
        return this
    }

    emit_mount() {
        for (var i = 0; i < this.children.length; i++) {
            this.children[i].emit_mount()
        }
        this.on_render()
        return this
    }

    on_render() { }

    on_mount() { }

    add_child(c: any) {
        c.mount(this.el)
        c.set_parent(this)
        c.index = this.children.length
        this.children.push(c)
        return c
    }

    set_parent(p: any) {
        this.parent = p
        return this
    }

    parse_child_option(o: Node) { }

    set_children(children: any, cls: any) {
        let visible_keys = new Set(children.map(c => c.key))
        for (let i = 0; i < children.length; i++) {
            this.parse_child_option(children[i])
            let key = children[i].key
            let child = this.children_map[key]
            if (!child) {
                child = cls(children[i])
                child.set_parent(this)
                this.children.push(child)
                this.children_map[key] = child
            }
            child.set_option(children[i]).show()
            child.index = i
            let refNode = this.el.childNodes[i]
            if (child.el !== refNode) {
                this.el.insertBefore(child.el, refNode || null)
            }
        }
        for (let key in this.children_map) {
            if (!visible_keys.has(key)) {
                this.children_map[key].hide()
            }
        }
        return this
    }

    get_tree_infos() {
        let p: Div | null = this
        let info: any[] = []
        while (p != null) {
            info.push({ index: p.index, type: this.node_type })
            p = p.parent
        }
        info.reverse()
        return info
    }

    set_title(s: string) {
        return this
    }

    set_option(option: any) {
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

    remove(i: number) { }

    render_option() { }

    add_children(children: any[]) {
        for (var i = 0; i < children.length; i++) {
            this.add_child(children[i])
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

    set_value(value: any) {
        return this
    }

    set_uri(uri: string, call_back?: any): this {
        web_dom.post(uri, {}, (ret: any) => {
            this.set_option(new Node().set_option(ret))
            call_back?.()
        })
        return this
    }
}

export interface Div extends DivStyleMethods { }

const divProto = Div.prototype as any
const styleProto = DivStyle.prototype as any
Object.getOwnPropertyNames(styleProto).forEach(name => {
    if (name !== 'constructor') {
        divProto[name] = styleProto[name]
    }
})
