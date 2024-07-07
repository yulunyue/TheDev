import { Div } from "../components/dom/div";

export class Dialog extends Div {
    init_style(): void {
        this.set_div_style({ position: "fixed" })
    }
    init_default_div_style() {

    }
    move_rb() {
        this.set_div_style({
            right: 0,
            bottom: 0
        })
        return this
    }
}
