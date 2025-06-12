import { Div } from "./div";
import Ct from "../../web/constant"
import web from "../../web/web_dom"
import { Node, to_node } from "../../web/cls";
import { Input } from "./input";
import { Button } from "./button";
import { Label } from "./label"
import Util from "../../tool/util"
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
export class BodyTd extends Td {
    init_style(): void {

    }
    render_option(): void {
        let ins = null
        if (this.option.type == "input") {
            ins = new Input().set_value(this.option.value)
        } else {
            ins = new Label().set_html(this.option.value)
        }
        this.ins = this.clear().add_child(ins)
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
    render_option(): void {
        this.field_map = {}

        this.clear().add_childs(this.option.childs.map(v => {
            this.field_map[v.key] = new BodyTd().set_option(v)
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
export class Tr extends Div {
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
            return new Td().set_option(v)
        }))
        return this
    }

    new_dom_row() {
        return new TrBody().set_option(this.option)
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
            return new Tr().set_option(v)
        }))
        return this
    }
}
export class Table extends Div {
    header_tr: Tr
    body_div: TBody
    head_div: Div
    constructor() {
        super("div")
    }
    init_body_div() {
        this.body_div = new TBody()
    }
    init_header_tr() {
        this.header_tr = new Tr()
    }
    init_head_div() {
        this.head_div = new Div().add_childs([
            new Div().set_style({ flexGrow: "1" }),
            new Input(),
            new Button().set_html("RUN")
        ]).set_style_flex(Ct.VERTICAL).set_style({ width: 1 })

    }
    init_node(): void {
        this.init_head_div()
        this.init_header_tr()
        this.init_body_div()
        this.add_childs([
            this.head_div,
            new Div("table").add_childs([
                new Thead().add_childs([
                    this.header_tr
                ]),
                this.body_div
            ])
        ]).full()
    }

    init_style() {
        this.set_style({
            textAlign: "left",
        })
    }
    set_header(items: Node[]) {
        this.header_tr.set_option(to_node({ childs: items }))
        return this
    }
    set_body(items: any[]) {
        this.body_div.clear()
        for (var i = 0; i < items.length; i++) {
            let td = this.header_tr.new_dom_row().set_data(items[i])
            this.body_div.add_child(td)
        }
        return this
    }
    set_data(data: any) {
        this.set_header(data.header)
        this.set_body(data.body)
        return this
    }
    render_option(): void {
        if (this.option.key) {
            this.http("table_get_all_data", (data: any) => {
                this.set_data(data)
            })
        } else {
            this.set_data(this.option.data)
        }
    }
    http(method: string, callback: any) {
        web.post(this.get_uri(method), {}, (v: Node) => {
            callback(v.data)
        })
    }
    get_uri(method: string) {
        return Util.uri_join([this.option.key, method])
    }
}
