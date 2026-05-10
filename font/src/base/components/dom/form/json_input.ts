import { Div } from "../div";
import Constant from "../../../web/constant";
export class JsonInput extends Div {
    el: HTMLTextAreaElement
    constructor() {
        super("textarea")
    }
    init_style(): void {
        this.set_style({
            width: `calc(100% - ${(Constant.DEFAULT_PADDING) * 2}px)`,
            height: 0.95,
            minHeight: 120,
            overflow: "auto",
            fontFamily: "monospace",
            fontSize: "13px",
            border: "none"
        })
    }
    set_value(value: any): this {
        if (typeof value == "string") {
            try {
                this._value = JSON.parse(value)
            } catch {
                console.log(value)
                this._value = { value: value }
            }
        } else {
            this._value = value
        }
        this.el.value = JSON.stringify(this._value, null, 2)
        return this
    }
    get_value(): any {
        try {
            this._value = JSON.parse(this.el.value)
        } catch {

        }
        return this._value
    }
}
