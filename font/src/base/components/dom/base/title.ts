import { Div } from "./div";

export class Title extends Div {
    init_style(): void {
        this.set_style({
            // alignItems: "center",
            // textAlign: "center"
        })
    }
    render_option(): void {
        this.set_value(this.option.value)
    }
    set_value(value: any): this {
        if (this.option.title) {
            value = this.option.title + ":" + value
        }
        this.set_html(value)
        return this
    }
}