import { Div } from "./div";
export class Select extends Div {
    constructor() {
        super("select")
    }
    render_option(): void {
        
    }
}
export function select() {
    return new Select()
}