import { Div } from "./div";

export class Progress extends Div {
    constructor() {
        super("progress")
    }
    set_max(v: any) {
        return this.set_attr("max", v)
    }
}
export function progress() {
    return new Progress()
}
export function progress_dev() {
    return new Progress().set_max(100).set_value(22)
}