import { Div } from "../../dom/div"
export class Span extends Div {
    constructor() {
        super("span")
    }
    set_value(value: any): this {
        return this.set_html(value)
    }
}
