import { Div } from "../div";
import Ct from "../../../web/constant"
import web from "../../../web/web_dom"
import { Node, to_node } from "../../../web/cls";
import { Input } from "../form/input";
import { Button, Buttons } from "../form/button";
import { Label } from "../base/label"
import { Pagination } from "../../combo/pagination";
import Util from "../../../tool/util"
import { Constant } from "../../export";
import { TrHead } from "./trhead";
import { TrBody } from "./trbody";
import { TBody } from "./tbody";
import { Thead } from "./thead";
import { Column } from "../../export";
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
    search_btn: Button
    init_style() {
        this.table_container.set_style({
            textAlign: "left",
            overflow: "auto",
            maxHeight: 600,
        })
        this.table.set_style({
            overflow: "auto",
            maxHeight: 600,
        })
        this.head_div.set_style({
            width: 1
        })
        this.table.set_style({ overflow: "auto" })
    }
    init_event(): void {
        this.search_btn.on_click(this.filter.bind(this))
    }
    init_node(): void {
        this.search_input = new Input().set_placeholder("关键字搜索")
        this.search_btn = new Button().set_html("搜索")
        this.head_div = new Div().add_childs([
            this.search_input,
            this.search_btn,
        ])
        this.body_div = new TBody()
        this.header_tr = new TrHead()
        this.table = new Div("table").add_childs([
            new Thead().add_childs([
                this.header_tr
            ]),
            this.body_div
        ])
        this.table_container = new Div().add_childs([
            this.table
        ])
        this.pagination = new Pagination()
        this.tail_div = new Div().add_childs([
            this.pagination
        ])
        this.add_childs([
            this.head_div,
            this.table_container,
            this.tail_div
        ])
    }
    hander_row_change(th: any) {
        let { idx, key, value } = th
        this.src_data.body[idx][key] = value
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


    set_header(items: Node[]) {
        this.header_tr.set_option({ childs: items })
        return this
    }
    filter() {
        let sv = this.search_input.get_value()
        this.option.data.rows = Util.filter_json_array(this.option.data.all_rows, sv)
        this.pagination.set_length(this.option.data.rows.length)
    }
    set_body(items: any[]) {
        this.option.data.all_rows = items
        this.pagination.on_change(this.show_body.bind(this))
        this.filter()
        return this
    }
    show_body() {
        this.body_div.clear()
        let idx = this.pagination.get_cur_idxs()

        for (var i = 0; i < idx.length; i++) {
            let data = this.option.data.rows[idx[i]]
            console.log(data)
            if (!data) {
                return
            }
            let td = this.header_tr.new_dom_row(idx[i]).set_data(data)
            this.body_div.add_child(td)
        }
    }
    draw(o: Node) {
        this.set_header(o.childs)
        this.set_body(o.value)
        return this
    }
    render_option(): void {
        if (this.option.url) {
            this.http("get", {}, (o: Node) => {
                this.draw(o)
            })
        } else {
            this.draw(this.option)
        }
    }
    http(method: string, data: any, callback: any) {
        web.post(this.get_uri(method), data, (v: Node) => {
            callback(v.data)
        })
    }
    get_uri(method: string) {
        return Util.uri_join([this.option.url, method])
    }
}