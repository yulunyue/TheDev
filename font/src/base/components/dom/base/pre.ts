import { Div } from "../div";
import web from "../../../web/web_dom"
import { Constant, Node } from "../../export";
export class Pre extends Div {
    constructor() {
        super("pre")
    }

    init_node(): void {

    }
    set_value(value: any): this {
        if (value instanceof Object) {
            value = JSON.stringify(value, null, 2)
        }
        return this.set_html(value)
    }
    init_style(): void {
        this.set_style({
            whiteSpace: "pre-wrap",
            overflowWrap: "break-word",
            // overflow: "auto"
        })
    }
    render_option() {
        this.set_value(this.option.value)
    }
}