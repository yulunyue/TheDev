import { Div } from "./div";

export class Title extends Div {
    init_style(): void {
        this.set_style({
            alignItems: "center",
            textAlign: "center"
        })
    }
    render_option(): void {
        this.set_html(this.option.get_title() + ":" + this.option.value)
    }
}