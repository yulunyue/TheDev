import { Div } from "./div";
import { Node } from "../../web/cls";
import Ct from "../../web/constant"
import web_dom from "../../web/web_dom"
import { Label } from "./base/label";
export class ListUi extends Div {
    data: any
    constructor() {
        super("div")
    }
    init_style(): void {
        this.set_style({
            overflowY: "auto"
        })
    }
    filter(s: any) {
        this.set_option({ filter_key: s })
    }
    get_row(o: Node) {
        let lb = new Label().set_border().set_option(o)
        return lb.on_click(() => this.do_change(this.option.key, null, lb.option))
    }
    get_data(key: string) {
        return this.data[key]
    }
    render_option(): void {
        this.option.data.size = 0
        this.data = {}
        if (this.option.children.length) {
            let children = []
            for (var i = 0; i < this.option.children.length; i += 1) {
                let v = this.option.children[i]
                if (v.title.indexOf(this.option.filter_key) != -1) {
                    children.push(v)
                }
                this.data[v.title] = v.value
            }
            this.option.data.size = children.length
            this.set_children(children, this.get_row.bind(this))

        }
    }
}