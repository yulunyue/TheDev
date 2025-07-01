import { Div } from "./div";
import Ct from "../../web/constant"
import web from "../../web/web_dom"
import { Node, to_node } from "../../web/cls";
import { Input } from "./input";
import { Button, Buttons } from "./button";
import { Label } from "./label"
import { Pagination } from "./pagination";
import Util from "../../tool/util"
import { Constant } from "../export";
export class Td extends Div {
    ins: Div
    constructor() {
        super("td", "")
    }
    render_option(): void {
        let ins = new Label().set_html(this.option.value)
        this.ins = this.clear().add_child(ins)
    }
}
export class Th extends Div {
    constructor() {
        super("th", "")
    }
    init_style(): void {
        this.set_style({
            position: "sticky",
            top: 0
        })
    }
    render_option(): void {
        this.set_html(this.option.title || this.option.value)
    }
}
export class BodyTd extends Td {
    row_idx: number
    set_row_idx(idx: number) {
        this.row_idx = idx
        return this
    }
    init_style(): void {

    }
    render_option(): void {
        let ins = null
        if (this.option.type == "input") {
            ins = new Input().set_value(this.option.value)
        }
        else if (this.option.type == 'btns') {
            ins = new Buttons().set_option(to_node({
                childs: this.option.value.map((v: any) => {
                    return { title: v }
                })
            }))
        }
        else {
            ins = new Label().set_html(this.option.title || this.option.value)
        }
        this.ins = this.clear().add_child(ins).on_change(() => {
            this._on_change({ idx: this.row_idx, key: this.option.key, value: this.ins.get_value() })
        })
    }
    set_value(value: any) {
        this.ins.set_value(value)
        return this
    }

}
export class TrBody extends Div {
    field_map: object
    constructor() {
        super("tr", "")
    }
    row_idx: number
    set_row_idx(idx: number) {
        this.row_idx = idx
        return this
    }
    render_option(): void {
        this.field_map = {}

        this.clear().add_childs(this.option.childs.map(v => {
            this.field_map[v.key] = new BodyTd().set_row_idx(
                this.row_idx
            ).on_change(this._on_change).set_option(v)
            return this.field_map[v.key]
        }))
    }
    set_data(data: any) {
        for (var key in this.field_map) {
            this.field_map[key].set_value(data[key])
        }
        return this
    }

}
export class TrHead extends Div {
    constructor() {
        super("tr", "")
    }
    init_style(): void {
        this.set_style({
            border: "1px solid #000"

        })
    }
    render_option() {
        this.clear().add_childs(this.option.childs.map(v => {
            return new Th().set_option(v)
        }))
        return this
    }

    new_dom_row(idx: number) {
        return new TrBody().set_row_idx(idx).on_change(this._on_change).set_option(this.option)
    }

}
export class Thead extends Div {
    constructor() {
        super("thead", "")
    }
    init_style(): void {

    }

}
export class TBody extends Div {
    constructor() {
        super("tbody", "")
    }
    init_style(): void {
        this.set_style({
            height: 400,
            overflowY: "auto"
        })
    }
    render_option() {
        this.clear().add_childs(this.option.childs.map(v => {
            let tr = new TrHead().set_option(v)
            return tr.on_change(this._on_change)
        }))
        return this
    }
}
export class Table extends Div {
    header_tr: TrHead
    body_div: TBody
    head_div: Div
    tail_div: Div
    table_container: Div
    pagination: Pagination
    search_input: Input
    table: Div
    src_data: any
    constructor() {
        super("div")
    }
    init_body_div() {
        this.body_div = new TBody()
        this.header_tr = new TrHead().on_change(
            (data: any) => {
                this.hander_row_change(data)
            }
        )
        this.table = new Div("table").add_childs([
            new Thead().add_childs([
                this.header_tr
            ]),
            this.body_div
        ]).set_style({ overflow: "auto" })
        this.table_container = new Div().add_childs([
            this.table
        ])

    }
    hander_row_change(th: any) {
        let { idx, key, value } = th
        this.src_data.body[idx][key] = value
    }
    init_tail_div() {
        this.pagination = new Pagination()
        this.tail_div = new Div().add_childs([
            new Div().set_flex_grow(1),
            this.pagination
        ]).set_style_flex(Constant.VERTICAL)
    }
    init_head_div() {
        this.search_input = new Input().set_placeholder("关键字搜索")
        this.head_div = new Div().add_childs([
            new Div().set_style({ flexGrow: "1" }),
            this.search_input,
            new Button().set_html("搜索").click(() => this.filter()),
            new Button().set_html("添加").click(() => this.add()),
            new Button().set_html("保存").click(() => this.save_all())
        ]).set_style_flex(Ct.VERTICAL).set_style({ width: 1 })

    }
    add() {
        return this
    }
    save_all() {
        if (this.option.key) {
            this.http("save", this.src_data, () => { })
        }
    }
    init_node(): void {
        this.init_head_div()
        this.init_body_div()
        this.init_tail_div()
        this.add_childs([
            this.head_div,
            this.table_container,
            this.tail_div
        ]).full()
    }

    init_style() {
        this.table_container.set_style({
            textAlign: "left",
            overflow: "auto",
            height: 600,
        })
        this.table.set_style({
            overflow: "auto",
            height: 600,
        })
        this.header_tr.set_style({
            position: "sticky",
            top: 0,
            zIndex: "10",
            backgroundColor: "#fff",
            border: "1px solid #000"
        })
    }
    set_header(items: Node[]) {
        this.header_tr.set_option(to_node({ childs: items }))
        return this
    }
    filter() {
        let sv = this.search_input.get_value()
        this.option.data.rows = Util.filter_json_array(this.option.data.all_rows, sv)

        this.pagination.set_length(this.option.data.rows.length)
    }
    set_body(items: any[]) {
        this.option.data.all_rows = items
        this.pagination.on_change(() => this.show_body())
        this.filter()
        return this
    }
    show_body() {
        this.body_div.clear()
        let page_size = this.pagination.page_size_select.get_value().value
        let start = this.pagination.cur_page.get_int() * page_size
        for (var i = start; i < page_size + start; i++) {
            let data = this.option.data.rows[i]
            if (!data) {
                break
            }
            let td = this.header_tr.new_dom_row(i).set_data(data)
            this.body_div.add_child(td)
        }
    }
    set_data(data: any) {
        this.src_data = data
        this.set_header(data.header)
        this.set_body(data.body)
        return this
    }
    render_option(): void {
        if (this.option.key) {
            this.http("get", {}, (data: any) => {
                this.set_data(data)
            })
        } else {
            this.set_data(this.option.data)
        }
    }
    http(method: string, data: any, callback: any) {
        web.post(this.get_uri(method), data, (v: Node) => {
            callback(v.data)
        })
    }
    get_uri(method: string) {
        return Util.uri_join([this.option.key, method])
    }
}
