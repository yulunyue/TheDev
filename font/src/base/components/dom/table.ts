import { Div } from "./div";
import Ct from "../../web/constant"
import web from "../../web/web_dom"
import { Node } from "../../web/cls";
import { Input } from "./input";
import { Button } from "./button";
import { Label } from "./label"
export class Td extends Div {
    ins: Div
    constructor() {
        super("td", "")
    }
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
    set_option(item: Node) {
        this.clear().add_childs(item.childs.map(v => {
            return new Td().set_option(v)
        }))
        return this
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
    }
    set_option(item: Node) {
        this.clear().add_childs(item.childs.map(v => {
            v.type = 'td'
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
    set_header(item: Node) {
        item.type = 'th'
        this.header_tr.set_option(item)
        return this
    }
    set_body(item: Node) {
        this.body_div.set_option(item)
        return this
    }
}
export function table() {
    return new Table().set_header(Ct.MOCK_NODE_3_5).set_body(Ct.MOCK_NODE_3_5)
}