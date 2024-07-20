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
        let int_value = parseInt(this.el.value)
        return isNaN(int_value) ? this.el.value : int_value
    }
    set_search(url: string) {
        web.bind_click(this.el, () => {
            web.post(url, { value: this.get_value() }, (node: Node) => {
                console.log(node, this.get_width())
            })
        })
        return this
    }

}
export function input() {
    return new Input()
}
export function search() {
    return new Input().set_search(Ct.MOCK_KEY)
}