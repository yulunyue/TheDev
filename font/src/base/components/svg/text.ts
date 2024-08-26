import { GNode } from "./gnode"
import { Node } from "../../web/cls"
export class Text extends GNode {
    constructor() {
        super("text")
    }
    init_style(): void {
        this.set_style({
            fontFamily: "Arial",
            dominantBaseline: "middle",
            textAnchor: 'middle',
            fontSize: 20,
            cursor: "pointer",
        })
    }
    set_option(option: Node): this {
        this.set_html(option.title)
        return this
    }
}
export function text() {
    return new Text()
}