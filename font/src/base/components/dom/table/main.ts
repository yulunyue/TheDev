import { Div } from "../div";
import Ct from "../../../web/constant"
import web from "../../../web/web_dom"
import { Node, to_node } from "../../../web/cls";
import { Input } from "../form/input";
import { Button } from "../form/button";
import { Label } from "../base/label"
import { Pagination } from "../../combo/pagination";
import Util from "../../../tool/util"
import { Constant, Row } from "../../export";
import { TrHead } from "./trhead";
import { TrBody } from "./trbody";
import { TBody } from "./tbody";
import { Thead } from "./thead";
import { Column } from "../../export";
import { Title } from "../form/title";
export class Table extends Row {
    header_tr: TrHead
    body_div: TBody
    head_div: Column
    head_title: Title
    tail_div: Column
    table_container: Div
    pagination: Pagination
    search_input: Input
    table: Div
    src_data: any
    search_btn: Button
    tail_left: Title
    init_style() {
        this.table_container.set_style({
            textAlign: "left",
            overflow: "auto",
            width: 1,
        })
        this.table.set_style({
            overflow: "auto",
            width: 1
        })
        this.head_title.set_flex(1)
        this.tail_left.set_flex(1)
        this.head_div.set_style({
            width: 1
        })
        this.search_input.set_style({ width: Constant.WIDTH_TEXT })
        this.set_style({ overflow: "auto" })


    }
    init_event(): void {
        this.search_btn.on_click(this.filter.bind(this))
        this.pagination.on_change(this.show_body.bind(this))
    }
    init_node(): void {
        this.search_input = new Input().set_placeholder("关键字搜索")
        this.search_btn = new Button().set_html("搜索")
        this.head_title = new Title()
        this.head_div = new Column().add_childs([
            this.head_title,
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
        this.tail_left = new Title()
        this.tail_div = new Column().add_childs([
            this.tail_left,
            this.pagination
        ])
        this.add_childs([
            this.head_div,
            this.table_container,
            this.tail_div
        ])
    }


    set_header(items: Node[]) {
        this.header_tr.set_option({ childs: items })
        return this
    }
    filter() {
        let sv = this.search_input.get_value()
        this.option.data.rows = Util.filter_json_array(this.option.data.all_rows, sv)
        this.pagination.set_length(this.option.data.rows.length)
        this.show_body()
    }
    set_body(items: any[]) {
        this.option.data.all_rows = items
        this.filter()
        return this
    }
    show_body() {
        this.body_div.clear()
        let idxs = this.pagination.get_cur_idxs()
        for (var i = 0; i < idxs.length; i++) {
            let data = this.option.data.rows[idxs[i]]
            if (!data) {
                return
            }
            let td = this.header_tr.new_dom_row(idxs[i]).set_data(data)
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
            this.http("to_table_view", {}, (o: Node) => {
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