
import { DivFactory } from "./base/div_factory"
import { Style, Node, Fn1, to_node, not_null, node } from "../../web/cls"

import { Div } from "./base/div"


export class Container extends Div {
    set_flex_style(direction: number, use_border?: boolean): this {
        this.set_style({
            flexGrow: this.size + "",
        })
        return this
    }
    set_option(option: Node): this {
        this.clear().add_child(DivFactory.new_div(option.type, option))
        return this
    }
}
export function container() {
    return new Container()
}
export function div(node_type?: string) {
    return new Div(node_type, "")
}
export { Div, DivFactory }