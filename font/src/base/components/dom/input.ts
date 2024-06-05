import { Div } from "./div";

export class Input extends Div {
    init_node() {
        this.el = Div.create_element("input")
    }
}
export default function () {
    return new Input()
}