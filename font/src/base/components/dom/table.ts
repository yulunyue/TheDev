import { Div } from "./div";
import Ct from "../../web/constant"
import web from "../../web/web_dom"
import { Node } from "../../web/cls";
export class Td extends Div {
    constructor() {
        super("td", "")
    }
}
export class Th extends Div {
    constructor() {
        super("th", "")
    }
}
export class Tr extends Div {
    constructor() {
        super("tr", "")
    }
    init_style(): void {

    }
    set_option(item: Node) {
        this.clear().add_childs(item.childs.map(v => {
            let ret = item.type == 'th' ? new Th() : new Td()
            return ret.set_html(v.title)
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
    constructor() {
        super("table")
        this.header_tr = new Tr()
        this.body_div = new TBody()
        this.add_childs([new Thead().add_child(this.header_tr), this.body_div])
    }
    init_style() {

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