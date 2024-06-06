import { Div } from "./div";
export class Select extends Div {
    init_node() {
        this.el = Div.create_element("select")
    }
}
export function select() {
    return new Select()
}