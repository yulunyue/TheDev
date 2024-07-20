import { Div } from "./div";
import Ct from "../../web/constant"
export class Table extends Div {
    constructor() {
        super("table")
    }
    set_header(path: any) {
        return this
    }
    set_row(path: any) {
        return this
    }
}
export function table() {
    return new Table().set_header(Ct.MOCK_KEY).set_row(Ct.MOCK_KEY)
}