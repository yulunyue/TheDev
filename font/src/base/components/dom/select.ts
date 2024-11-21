import { Div } from "./div";
import { Constant } from "../export";
import web from "../../web/web_dom"
import { Node, to_node } from "../../web/cls";
export class SeOption extends Div {
    constructor() {
        super("option")
    }
    render_option(): void {
        this.set_html(this.option.title)
    }
}
export class Select extends Div {
    el: HTMLSelectElement
    constructor() {
        super("select")
    }
    init_node(): void {

    }
    init_style(): void {
        this.set_style({
            minWidth: Constant.INPUT_STRING_MIN_WIDTH,
            margin: Constant.DEFAULT_MARGIN,
            padding: Constant.DEFAULT_PADDING,
            border: "1px solid #ccc"
        })
    }
    init_event(): void {
        web.bind_change(this.el, () => {
            this.do_change()
        })
    }
    set_uri(uri: string) {
        web.post(uri, {}, (node: Node) => {
            this.option.childs = to_node(node).childs
            this.render_child()
        })
        return this
    }
    render_child() {
        this.clear()
        for (var i = 0; i < this.option.childs.length; i++) {
            let op = this.option.childs[i]
            this.add_child(new SeOption().set_option(op).set_value(i))
        }
        this.do_change()
    }
    get_value() {
        return this.option.childs[this.el.value]
    }
    render_option(): void {
        if (this.option.data.uri) {
            this.set_uri(this.option.data.uri)
        } else if (this.option.childs) {
            this.render_child()
        }
    }
}
export function select() {
    return new Select()
}