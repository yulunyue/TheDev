import { Div } from "./div";
export class Select extends Div {
    constructor() {
        super("select")
    }
}
export function select() {
    return new Select()
}