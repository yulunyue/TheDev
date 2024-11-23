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
        this.set_style({
            outline: "none",
            margin: Constant.DEFAULT_MARGIN,
            padding: Constant.DEFAULT_PADDING
        })
    }
    render_option() {
        this.set_value(this.option.value)
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
export class TextArea extends Div {
    el: HTMLTextAreaElement
    constructor() {
        super("textarea")
    }
    init_style(): void {
        this.set_style({
            width: Constant.TEXT_AREA_WIDTH,
            height: Constant.TEXT_AREA_HEIGHT_1,
            overflow: "auto"
        })
    }
    get_value() {
        console.log(this.el.value)
        return this.el.value
    }

}
export function input() {
    return new Input()
}
export function text_area() {
    return new TextArea()
}