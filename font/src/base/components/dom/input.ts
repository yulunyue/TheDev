import { Div } from "./div";
import web from "../../web/web_dom"
import Ct from "../../web/constant"
import { Node } from "../../web/cls";
export class Input extends Div {
    el: HTMLInputElement
    constructor() {
        super("input")
    }
    init_node() {

    }

    init_style(): void {
        this.set_style({ outline: "none" })
    }
    on_click() {

    }
    get_value() {
        return this.el.value
    }
    get_int() {
        return parseInt(this.get_value())
    }

}
export function input() {
    return new Input()
}