import { Div } from "../div";
import { Style, Node, Fn1 } from "../../../web/cls"
import Constant from "../../../web/constant";
export class Button extends Div {
    constructor() {
        super("button")
    }
    init_node() {

    }
    set_value(value: any): this {
        this.set_html(value)
        return this
    }
    init_style(): void {
        this.set_style({
            outline: "none",
            margin: Constant.DEFAULT_MARGIN,
            padding: Constant.DEFAULT_PADDING
        })
    }
}

