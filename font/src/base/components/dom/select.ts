import { Div } from "./div";
import { Constant } from "../export";
import web from "../../web/web_dom"
import { Node, to_node } from "../../web/cls";
export class Li extends Div {
    constructor() {
        super("li")
    }
    render_option() {
        console.log(this.option)
        this.set_html(this.option.title)
    }
}
export class Select extends Div {
    constructor() {
        super("select")
    }
    init_node(): void {
        this.set_style({
            minWidth: Constant.INPUT_STRING_MIN_WIDTH
        })
    }
    init_event(): void {
        web.bind_change(this.el, () => {
            this.option.value = this.get_value()
        })
    }
    set_uri(uri: string) {
        web.post(uri, {}, (node: Node) => {

            this.option.childs = node.childs
            this.render_child()
        })
    }
    render_child() {
        this.clear().add_childs(this.option.childs.map(v => {
            new Li().set_option(v)
        }))
    }
    render_option(): void {
        if (this.option.data.uri) {
            this.set_uri(this.option.data.uri)
        }
    }
}
export function select() {
    return new Select()
}