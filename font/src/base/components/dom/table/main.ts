import { Div } from "../div";
import Ct from "../../../web/constant"
import web from "../../../web/web_dom"
import { Node, to_node } from "../../../web/cls";
import { Input } from "../input";
import { Button, Buttons } from "../button";
import { Label } from "../label"
import { Pagination } from "../pagination";
import Util from "../../../tool/util"
import { Constant } from "../../export";
import { TrHead } from "./trhead";
import { TrBody } from "./trbody";
import { TBody } from "./tbody";
import { Thead } from "./thead";
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
            new Button().set_html("搜索").on_click(() => this.filter()),
            new Button().set_html("添加").on_click(() => this.add()),
            new Button().set_html("保存").on_click(() => this.save_all())
        ]).set_style_flex(Ct.VERTICAL).set_style({ width: 1 })

    }
    add() {
        this.header_tr.add_one_row()
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