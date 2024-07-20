import { Div } from "./div";
import web from "../../web/web_dom"
export class Input extends Div {
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
    set_search(url: string) {
        web.bind_click(this.el, this.on_click)
        return this
    }

}
export function input() {
    return new Input()
}
export function search() {
    return new Input()
}