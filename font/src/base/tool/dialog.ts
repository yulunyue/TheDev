import { Div } from "../components/dom/div";

export class Dialog extends Div {
    init_style(): void {
        this.set_div_style({ position: "fixed" })
    }
    move_rb() {
        return this
    }
}
