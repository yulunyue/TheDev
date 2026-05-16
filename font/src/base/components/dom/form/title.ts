import { Div } from "../div";
import { Button } from "./button";
export class Title extends Div {
    title: Div
    btns: Button[]
    init_node(): void {
        this.title = this.add_child(new Div()).set_size(1)
    }
    set_btns(btns: Button[]) {
        this.add_children(btns)
        return this
    }
}
