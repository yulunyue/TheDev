import { Div } from "../div";
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