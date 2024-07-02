import { Div } from "./div";
export class Select extends Div {
    constructor() {
        super("select")
    }
    init_node() {

    }
}
export function select() {
    return new Select()
}