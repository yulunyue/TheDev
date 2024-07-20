import { Div } from "./div";
export class ListUi extends Div {
    set_list(path: any) {
        return this
    }
}
export function listui() {
    return new ListUi().set_list("label")
}