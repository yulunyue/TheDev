import { Div } from "./div";
import Constant from "../../web/constant";
export class Input extends Div {
    el: HTMLInputElement
    constructor() {
        super("input")
    }
    init_node() {

    }

    init_style(): void {
        this.set_style({ outline: "none",           
             margin: Constant.DEFAULT_MARGIN,
            padding: Constant.DEFAULT_PADDING })
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