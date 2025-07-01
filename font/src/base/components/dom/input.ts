import { Div } from "./div";
import { Title, Button } from "./button";
import Constant from "../../web/constant";
export class Input extends Div {
    el: HTMLInputElement
    constructor() {
        super("input")
    }
    init_node() {

    }
    set_placeholder(title: string) {
        return this.set_attr("placeholder", title)
    }
    init_style(): void {
        this.set_style({
            outline: "none",
            margin: Constant.DEFAULT_MARGIN,
            padding: Constant.DEFAULT_PADDING
        })
    }
    render_option() {
        if (this.option.type == Constant.NUMBER) {
            this.set_width(Constant.INPUT_NUMBER_WIDTH)
        }
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
    on_change(call: any): this {
        // this.el.onchange = call
        this.el.oninput = call
        return this
    }

}
export class TextArea extends Div {
    el: HTMLTextAreaElement
    constructor() {
        super("textarea")
    }
    init_style(): void {
        this.set_style({
            width: 0.95,
            height: 0.95,
            overflow: "auto"
        })
    }

    get_value() {
        return this.el.value
    }

}
export function input() {
    return new Input()
}
export class TextAreaRich extends Div {
    area: TextArea
    title: Title

    init_node(): void {
        this.title = this.add_child(new Title())
        this.area = this.add_child(new TextArea())
    }
    set_title(s: string) {
        this.title.title.set_html(s)
        return this
    }
    set_value(value: any): this {
        this.area.set_value(value)
        return this
    }
    get_value() {
        return this.area.get_value()
    }
    set_btns(btns: any) {
        this.title.set_btns(btns)
        return this
    }
    set_flex_style() {
        return this
    }
}
export function text_area() {
    return new TextAreaRich()
}